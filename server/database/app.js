const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');
const app = express();
const port = 3030;

app.use(cors());
app.use(require('body-parser').urlencoded({ extended: false }));
app.use(express.json());

const reviewsPath = fs.existsSync("./data/reviews.json") ? "./data/reviews.json" : "reviews.json";
const dealershipsPath = fs.existsSync("./data/dealerships.json") ? "./data/dealerships.json" : "dealerships.json";

let reviews_data = JSON.parse(fs.readFileSync(reviewsPath, 'utf8'));
let dealerships_data = JSON.parse(fs.readFileSync(dealershipsPath, 'utf8'));

let inMemoryReviews = [...reviews_data['reviews']];
let inMemoryDealers = [...dealerships_data['dealerships']];

const Reviews = require('./review');
const Dealerships = require('./dealership');

let isMongoConnected = false;
mongoose.connect(process.env.MONGO_URL || "mongodb://mongo_db:27017/", { 'dbName': 'dealershipsDB' })
  .then(() => {
    isMongoConnected = true;
    console.log("Connected to MongoDB");
    Reviews.deleteMany({}).then(() => {
      Reviews.insertMany(reviews_data['reviews']);
    });
    Dealerships.deleteMany({}).then(() => {
      Dealerships.insertMany(dealerships_data['dealerships']);
    });
  })
  .catch((err) => {
    console.log("MongoDB connection deferred. Utilizing embedded JSON records:", err.message);
  });

// Express route to home
app.get('/', async (req, res) => {
  res.send("Welcome to the Mongoose API");
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    if (isMongoConnected) {
      const documents = await Reviews.find();
      return res.json(documents);
    }
    res.json(inMemoryReviews);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const dealerId = parseInt(req.params.id);
    if (isMongoConnected) {
      const documents = await Reviews.find({ dealership: req.params.id });
      return res.json(documents);
    }
    const filtered = inMemoryReviews.filter(
      (r) => r.dealership === dealerId || r.dealership == req.params.id
    );
    res.json(filtered);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    if (isMongoConnected) {
      const documents = await Dealerships.find();
      return res.json(documents);
    }
    res.json(inMemoryDealers);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch Dealers by a particular state
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    if (isMongoConnected) {
      const documents = await Dealerships.find({ state: req.params.state });
      return res.json(documents);
    }
    const filtered = inMemoryDealers.filter(
      (d) =>
        d.state.toLowerCase() === req.params.state.toLowerCase() ||
        (d.st && d.st.toLowerCase() === req.params.state.toLowerCase())
    );
    res.json(filtered);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch dealer by a particular id
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const dealerId = parseInt(req.params.id);
    if (isMongoConnected) {
      const documents = await Dealerships.find({ id: dealerId });
      return res.json(documents);
    }
    const found = inMemoryDealers.filter((d) => d.id === dealerId);
    res.json(found);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to insert review
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  try {
    let data = req.body;
    if (typeof data === 'string' || Buffer.isBuffer(data)) {
      data = JSON.parse(data.toString());
    }
    let new_id = 1;
    if (isMongoConnected) {
      const documents = await Reviews.find().sort({ id: -1 });
      if (documents.length > 0) new_id = documents[0]['id'] + 1;
      const review = new Reviews({
        id: new_id,
        name: data['name'],
        dealership: data['dealership'],
        review: data['review'],
        purchase: data['purchase'],
        purchase_date: data['purchase_date'],
        car_make: data['car_make'],
        car_model: data['car_model'],
        car_year: data['car_year'],
      });
      const savedReview = await review.save();
      return res.json(savedReview);
    } else {
      if (inMemoryReviews.length > 0) {
        new_id = Math.max(...inMemoryReviews.map((r) => r.id)) + 1;
      }
      const review = {
        id: new_id,
        name: data['name'],
        dealership: parseInt(data['dealership']) || data['dealership'],
        review: data['review'],
        purchase: data['purchase'],
        purchase_date: data['purchase_date'],
        car_make: data['car_make'],
        car_model: data['car_model'],
        car_year: data['car_year'],
      };
      inMemoryReviews.push(review);
      return res.json(review);
    }
  } catch (error) {
    console.log(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
