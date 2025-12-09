// map_frontend.js

// Replace 'YOUR_API_KEY' with your actual Google Maps JavaScript API Key
const GOOGLE_MAPS_API_KEY = 'YOUR_API_KEY';
const API_ENDPOINT = '/api/resources/map'; // Flask API endpoint

let map;

/**
 * Initializes the Google Map.
 */
function initMap() {
    // Default center (e.g., your campus coordinates)
    const defaultCenter = { lat: 37.3382, lng: -121.8863 }; 
    
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15,
        center: defaultCenter,
        mapId: 'RESOURCE_MAP' // Use a Map ID for custom styling
    });

    fetchResourceData();
}

/**
 * Fetches resource data from the Flask API and places markers on the map.
 */
async function fetchResourceData() {
    try {
        const response = await fetch(API_ENDPOINT);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const markersData = await response.json();
        
        markersData.forEach(placeMarker);
    } catch (error) {
        console.error("Could not fetch resource data:", error);
        alert("Error loading resource locations. Check the console for details.");
    }
}

/**
 * Places a single marker on the map with a custom icon and info window.
 * @param {Object} data - Resource object from the Flask API.
 */
function placeMarker(data) {
    const position = { lat: data.lat, lng: data.lng };
    
    // Define the custom icon based on the 'icon' and 'color' data from the API
    const iconBaseUrl = '{{ url_for("static", filename="images/") }}';
    const icon = {
        url: iconBaseUrl + data.icon, // Path to your custom icon image (e.g., health.png)
        scaledSize: new google.maps.Size(32, 32),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(16, 16)
    };

    const marker = new google.maps.Marker({
        position: position,
        map: map,
        title: data.service,
        icon: icon 
    });

    // Info Window content
    let contentString = `
        <div id="content">
            <h3 id="firstHeading" class="firstHeading">${data.service}</h3>
            <p><strong>Type:</strong> ${data.type}</p>
            ${data.link ? `<p><a href="${data.link}" target="_blank">View Details</a></p>` : ''}
        </div>
    `;

    const infoWindow = new google.maps.InfoWindow({
        content: contentString,
    });

    // Add click listener to show info window
    marker.addListener("click", () => {
        infoWindow.open({
            anchor: marker,
            map,
            shouldFocus: false,
        });
    });
}

// Ensure the Google Maps API loads this script and calls initMap
// This script needs to be loaded *after* the main Google Maps script tag.
// For example:
// <script async defer src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap"></script>
