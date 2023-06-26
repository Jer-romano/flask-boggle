$(document).ready(function() {
    $("#word-form").on("submit", submitGuess);
    let startForm = $("#start-form");
    let startBtn = $("#start-btn");
    let restartBtn = $("#restart-btn");

    let score = 0;
    const timerVal = 60;
    
    class Timer {
        constructor(startVal, domEl) {
            this.startVal = startVal;
            this.currentVal = startVal;
            this.intervalId = 0;
            this.domElement = domEl;
            console.log(this.startVal, this.domElement)
            this.domElement.text(this.startVal);
        }
        endGame() {
            $("#guess-btn").attr("disabled", "disabled");
            $("#times-up-msg").removeClass();
            submitScore(score);
        }
    
        startTimer() {
            this.intervalId = setInterval(() => this.decreaseTimer(), 1000);
        }
    
        decreaseTimer() {
            if (this.currentVal == 0) {
                clearInterval(this.intervalId);
                this.endGame();
            } else {
                this.currentVal -= 1;
                this.updateDom();
            }
        }
    
        updateDom() {
            if(this.currentVal < 10) {
                this.domElement.text("0" + this.currentVal);
            } else {
                this.domElement.text(this.currentVal);
            }
        }
     
    
    }
    if(window.location.pathname == "/start") {
        let timer = $("#timer");
        let timerObj = new Timer(timerVal, timer);
        timerObj.startTimer();
     }
    
    // $(document).on("click", "#start-btn", function(evt) {
    //     evt.preventDefault();
    //     let timer = $("#timer");
    //     let timerObj = new Timer(timerVal, timer);
       
    //    timerObj.startTimer();
    // });
    
    async function submitGuess(evt) {
        evt.preventDefault();
        $("#response").text("");
        let guess = $("#guess").val();
        guess = guess.toLowerCase();
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
        let is_unique = response.data["is-unique"];
        console.log("Unique:", is_unique);
        updateGameInfo(result, guess, is_unique);
    
        $("#guess").val("");
    }

    async function submitScore(localScore) {
        try {
            const response = await axios.request({
                url: "http://127.0.0.1:5000/endgame",
                method: "POST",
                data: {score: localScore}
            });
            let { high_score } = response.data;
            $("#high-score").text(high_score);
        } catch(err) {
            console.error("submitScore function failed: ", err);
        }
       restartBtn.removeClass();
      
    }

    function updateGameInfo(result, guess, is_unique) {
        if (result == "ok" && is_unique) {
            $("#response").text("Nice find!");
            $("#found-words-list").append($(`<span>${guess},</span>`));
            score += guess.length;
            $("#score-value").text(score);
        }
        else if (result == "not-on-board") {
            $("#response").text(`"${guess}" is not present.`);
        }
        else if (result == "not-word") {
            $("#response").text(`"${guess}" is not a valid English word.`);
        }
        else {
            $("#response").text(`"${guess}" has already been found.`);
        }
    }

    async function restartGame(evt) {
        $("#response").text("");
        $("#score-value").text("0");
        $("#times-up-msg").addClass("hidden");

        // axios.get("/restart")
        // .then(function(response) {
        //     console.log("Restart Response:", response);
        // })
        // .catch(function(error) {
        //     console.error("restartGame function failed: ", err);
        // })
        // .finally(function() {
        //     $("#restart-btn").addClass("hidden");
        // })
        // try {
        //     const response = await axios.request({
        //         url: "http://127.0.0.1:5000/restart",
        //         method: "POST",
        //     });
        //     console.log("Restart Response:", response);
        // } catch(err) {
        //     console.error("restartGame function failed: ", err);
        // }
    }
    restartBtn.click(restartGame);
});

