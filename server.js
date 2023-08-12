const express = require("express");
const bodyParser = require("body-parser");
const axios = require("axios");
const fs = require("fs");
const path = require("path");

const app = express();
const port = 3010;

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.use(express.static(path.join(__dirname, "public"))); // Serve static files from the "public" directory

app.post("/upload", async (req, res) => {
    try {
        const file = req.files.file; // Assuming you're using a middleware to handle file uploads
        const fileName = file.name;
        const filePath = path.join(__dirname, "public", "uploads", fileName); // Store files in the "uploads" directory

        // Save the file to the server
        file.mv(filePath, async (error) => {
            if (error) {
                console.error("Error saving file:", error);
                return res.status(500).json({ message: "Error uploading file" });
            }

            // Example Discord webhook URL
            const discordWebhook = "https://discord.com/api/webhooks/1139686248496246825/blHegQ65BCmPE93qBe8tlMyE3IP6RqQStAetrBOp4Mi7kZRgV1xVNDI2d7TmDwjU5Aln";

            // Send file to Discord webhook
            const response = await axios.post(discordWebhook, {
                content: "New file uploaded!",
                // Include other information here if needed
            });

            console.log("File uploaded to Discord:", response.data);

            res.json({ message: "File uploaded successfully" });
        });
    } catch (error) {
        console.error("Error uploading file to Discord:", error);
        res.status(500).json({ message: "Error uploading file" });
    }
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
