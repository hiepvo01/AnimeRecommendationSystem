var refreshButton = document.getElementById("refreshButton");

//add events to those 2 buttons
refreshButton.addEventListener("click", refresh);

const get_similar = new WebSocket("ws://127.0.0.1:8000/search_similar");
const get_full = new WebSocket("ws://127.0.0.1:8000/search_full");
const button1 = document.querySelector("#request_similar");
const button2 = document.querySelector("#request_full");

get_similar.onopen = (event) => {
    console.log("WebSocket similar is open now.");
};

get_similar.onclose = (event) => {
    console.log("WebSocket similar is closed now.");
};

get_full.onopen = (event) => {
    console.log("WebSocket full is open now.");
};

get_full.onclose = (event) => {
    console.log("WebSocket full is closed now.");
};

get_similar.onmessage = (event) => {
  // append received message from the server to the DOM element 
  const similar_name = document.querySelector("#similar_name");
  similar_name.innerHTML += event.data;
};

get_full.onmessage = (event) => {
    // append received message from the server to the DOM element 
    const full_name = document.querySelector("#full_name");
    full_name.innerHTML += event.data;
  };

button1.addEventListener("click", () => {
  const similars = document.querySelector("#search_similar");
  const data = `${similars.value}`;
  console.log(data)

  // Send composed message to the server
  get_similar.send(data);

  // clear input fields
  similars.value = "";
});

button2.addEventListener("click", () => {
    const fulls = document.querySelector("#search_full");
    const data = `${fulls.value}`;
    console.log(data)
  
    // Send composed message to the server
    get_full.send(data);
  
    // clear input fields
    fulls.value = "";
  });
  
function refresh() {
    location.reload();
}