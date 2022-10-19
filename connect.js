// connection to database
import mongoose from "mongoose";
let conn;

const connect = async () => {
    let dbUrl = "mongodb+srv://kai:Shared123@clusterzero.txf5k.mongodb.net/ioe_project?retryWrites=false&w=majority"
	const mongoOptions = {
		serverSelectionTimeoutMS: 5000,
		retryWrites: true,
	};

	try {
		conn = mongoose.connect(dbUrl, mongoOptions);
		console.log({
			message: `Connected to MongoDB`,
			url: dbUrl,
		});
	} catch (error) {
		console.log({
			message: `Error connecting to MongoDB`,
			error: error.message,
		});
	}
	return conn;
};

export default connect;
