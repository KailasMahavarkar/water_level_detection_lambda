import mongoose from "mongoose";
const Schema = mongoose.Schema;


const baseSchema = new Schema({
    _id: {
        type: mongoose.Schema.Types.ObjectId,
        auto: true,
    },
    log: {
        type: Array,
        required: true,
        default: []
    }
});

const logModel = mongoose.model("log", baseSchema);
export default logModel;
