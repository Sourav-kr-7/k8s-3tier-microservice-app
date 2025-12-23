FROM nginx:1.27-alpine

# Serve static assets from the default nginx html directory.
WORKDIR /usr/share/nginx/html
COPY index.html styles.css ./
# Custom nginx config wires /api to the backend service name.
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
# Default nginx entrypoint keeps the container running.
CMD ["nginx", "-g", "daemon off;"]

