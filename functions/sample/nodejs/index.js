/**
 * Get all databases
 */

const express = require("express");
const fs = require("fs");
const app = express();
const port = 3000; // Change this to your desired port

// Middleware to handle JSON
app.use(express.json());

// Load the dealership data from the JSON file
const dealershipData = JSON.parse(fs.readFileSync("dealership.json"));

// Create an endpoint for /api/dealership
app.get("/api/dealership", (req, res) => {
  const { state } = req.query;

  if (!state) {
    res.status(400).json({ error: "State parameter is required" });
    return;
  }

  const filteredDealerships = dealershipData.dealerships.filter(
    (dealer) => dealer.state === state
  );

  if (filteredDealerships.length === 0) {
    // Send a 404 response if the state does not exist
    res.status(404).json({ error: "The state does not exist" });
  } else {
    // Send the list of dealerships from the state
    res.json(filteredDealerships);
  }
});

// Load the review data (assuming you have a review.json file)
const reviewData = require("./review.json");

// ...

// Create an endpoint for /api/review
app.get("/api/review", (req, res) => {
  const { dealerId } = req.query;

  if (!dealerId) {
    res.status(400).json({ error: "dealerId parameter is required" });
    return;
  }

  const filteredReviews = reviewData.filter(
    (review) => review.dealership == dealerId
  );

  if (filteredReviews.length === 0) {
    // Send a 404 response if the dealerId does not exist
    res.status(404).json({ error: "dealerId does not exist" });
  } else {
    // Send the list of reviews for the given dealership
    res.json(filteredReviews);
  }
});

app.use(bodyParser.json()); // Add support for parsing JSON in requests

// Create an array to store reviews (you can use a database instead)
let reviews = [];

// ...

// Create an endpoint for posting a review to /api/review
app.post("/api/review", (req, res) => {
  const newReview = req.body.review;

  if (!newReview) {
    res.status(400).json({ error: "Invalid request body" });
    return;
  }

  // Simulate adding the review to your data store (in this case, the array)
  reviews.push(newReview);

  // Send a success response
  res.status(201).json(newReview); // You can adjust the status code if needed
});

// Handle 500 errors
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: "Something went wrong on the server" });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

// -----------------------------------------------------------------------------------------

const { CloudantV1 } = require("@ibm-cloud/cloudant");
const { IamAuthenticator } = require("ibm-cloud-sdk-core");

function main(params) {
  const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
  const cloudant = CloudantV1.newInstance({
    authenticator: authenticator,
  });
  cloudant.setServiceUrl(params.COUCH_URL);

  let dbList = getDbs(cloudant);
  return { dbs: dbList };
}

function getDbs(cloudant) {
  cloudant
    .getAllDbs()
    .then((body) => {
      body.forEach((db) => {
        dbList.push(db);
      });
    })
    .catch((err) => {
      console.log(err);
    });
}
