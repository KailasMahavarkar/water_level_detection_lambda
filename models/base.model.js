import mongoose from "mongoose";
const Schema = mongoose.Schema;

let rawDate = new Date().toISOString();
let today = rawDate.slice(0, 10);

const baseSchema = new Schema({
    _id: {
        type: String,
        required: true,
        default: today
    },
    data: {
        type: Array,
        required: true,
        default: []
    }
});

const baseModel = mongoose.model("base", baseSchema);
export default baseModel;
