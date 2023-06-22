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
            this.stopTimer(this.intervalId);
        } else {
            this.currentVal -= 1;
            console.log(this.currentVal);
        }
    }

    stopTimer(id) {
        clearInterval(id);
    }
}

timer = new Timer(10);
timer.startTimer();
