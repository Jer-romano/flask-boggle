$(document).ready(function() {
    $("#word-form").on("submit", submitGuess);
    let startForm = $("#start-form");
    let startBtn = $("#start-btn");
     
    let score = 0;
    let timerVal = 59;
    
    class Timer {
        constructor(startVal, domEl) {
            this.startVal = startVal;
            this.currentVal = startVal;
            this.intervalId = 0;
            this.domElement = domEl;
        }
    
        startTimer() {
            this.intervalId = setInterval(() => this.decreaseTimer(), 1000);
        }
    
        decreaseTimer() {
            if (this.currentVal == 0) {
                clearInterval(this.intervalId);
                disableForm();
            } else {
                this.currentVal -= 1;
                this.updateDom();
            }
        }
    
        updateDom() {
            this.domElement.text(this.currentVal);
           //document.getElementById("timer").textContent = this.currentVal;
        }
    
    }
    
    
    $(document).on("click", "#start-btn", function(evt) {
        let timer = $("#timer");
        let timerObj = new Timer(59, timer);
       // evt.preventDefault();
       timerObj.startTimer();
    });
    
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
        console.log(result);
        updateGameInfo(result, guess);
    
        $("#guess").val("");
    }

    function disableForm() {
        $("#word-form").attr("disabled", "disabled");
    }
    
    function updateGameInfo(result, guess) {
        if (result == "ok") {
            $("#response").text("Nice find!");
            $("#found-words").append($(`<li> ${guess} </li>`));
            score += guess.length;
            $("#score-value").text(score);
        }
        else if (result == "not-on-board") {
            $("#response").text(`${guess} is not present.`);
        }
        else {
            $("#response").text(`${guess} is not a valid English word.`);
        }
    }
});

