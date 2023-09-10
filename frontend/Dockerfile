# Use an official Node runtime as the base image
FROM node:14

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY package*.json ./

# Install any needed packages using npm
RUN npm install

# Copy the rest of the application code
COPY . .

# Make port 3000 available to the world outside this container (if you use React's dev server)
EXPOSE 3000

# Define environment variable (if needed, like REACT_APP_...)
# ENV REACT_APP_MY_VAR value

# Run npm start when the container launches (or build command if you're building inside the container)
CMD ["npm", "start"]
