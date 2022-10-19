import serverless from "serverless-http";
import express from 'express';
import connect from './connect.js';
import baseModel from "./models/base.model.js";
import logModel from "./models/log.model.js";

const app = express();

// body parser
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// json space
app.set('json spaces', 2);

const runOnError = async (res, error) => {
    await logModel.updateOne({
        tag: "log"
    }, {
        $push: {
            logs: JSON.stringify(error)
        }
    })
    res.status(500).json({
        message: "Error",
        error: error.message,
    })
}

const generateData = (distance, level) => {
    return {
        "time": Date.now(),
        "distance": eval(distance) || 0,
        "level": eval(level) || 0
    }
}

app.get('/hook', async (req, res) => {
    const distance = req.body.distance || req.query.distance;
    const level = req.body.level || req.query.level;

    let rawDate = new Date().toISOString();
    let today = rawDate.slice(0, 10);

    const doesTodayExist = await baseModel.exists({
        _id: today
    })



    if (doesTodayExist) {
        try {
            await baseModel.updateOne({
                _id: today
            }, {
                $push: {
                    data: generateData(distance, level)
                }
            })

            return res.status(200).json({
                message: "Data updated successfully"
            })

        } catch (error) {
            return runOnError(res, error);
        }
    }

    // today does not exist
    const newBase = new baseModel({
        _id: today,
        data: [
            generateData(distance, level)
        ]
    })

    try {
        const saveRes = await newBase.save();
        return res.status(200).json({
            message: "new date added successfully",
            data: saveRes
        })
    } catch (error) {
        return runOnError(res, error);
    }


})

app.get('/', (req, res) => {
    // console.log("req -->", req);

    return res.json({
        message: 'hook is working'
    })
})

const handlerMaker = serverless(app);
const handler = async (context, req) => {
    await connect()
    return await handlerMaker(context, req);
};

export { app, handler };