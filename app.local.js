import { app } from './app.js';
import connect from './connect.js';

app.listen(2000, async () => {
    await connect()
    console.log('Server is running on port 2000');
})