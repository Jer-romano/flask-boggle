$("#word-form").on("submit", submitGuess);
 
let score = 0;

async function submitGuess(evt) {
    evt.preventDefault();
    let guess = $("#guess").val();
    let response;
    try {
        response = await axios.request({
            url: "http://127.0.0.1:5000/submit",
            method: "POST",
            data: {word: guess}
        })
    } catch(err) {
        console.error("submitGuess function failed: ", err);
    }
    let result = response.data["result"];
    $("#response").text(result);
    if (result == "ok") {
        $("#found-words").append($(`<li> ${guess} </li>`));
        score += guess.length;
        $("#score-keeper").text(score);
    }
    $("#guess").val("");
}