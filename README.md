# World Seed

World Seed is an AI-assisted tool for worldbuilding and storytelling. The system works with entities, which can be customized with any number of user-defined attributes. These attributes can either be manually entered by users or automatically generated. Users can then select multiple entities to create scenes, providing specific instructions for how they want the scene to unfold. The system can then analyze the entities' attributes, combined with user inputs, to generate possibilities for how the scene might play out.

## Getting Started

**Backend**

Make sure you have `poetry` and `docker` installed.

- `docker compose up db` to start Postgres
- `cd backend && ./dev.sh` to start the server

**Frontend**

Make sure you have a reasonably new Node.js installed (I'm running v20.17.0)

- `npm install`
- `npm run dev`
- Open up `http://localhost:5173` in your browser
