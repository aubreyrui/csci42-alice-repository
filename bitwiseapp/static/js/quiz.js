const url = window.location.href;
console.log(url);

const quizBox = document.getElementById('quiz-box');
const timerBox = document.getElementById('timer-box');

let timerInterval; // Variable to hold the timer interval

const activateTimer = (time) => {
    // First state
    if (time.toString().length < 2) {
        timerBox.innerHTML = `<b>0${time}:00</b>`;
    } else {
        timerBox.innerHTML = `<b>${time}:00</b>`;
    }

    // countdown
    let minutes = time - 1;
    let seconds = 60;

    let displaySeconds;
    let displayMinutes;

    timerInterval = setInterval(() => { // Assign the interval to the variable
        seconds--;
        if (seconds < 0) {
            seconds = 59;
            minutes--;
        }
        if (minutes.toString().length < 2) {
            displayMinutes = '0' + minutes;
        } else {
            displayMinutes = minutes;
        }

        if (seconds.toString().length < 2) {
            displaySeconds = '0' + seconds;
        } else {
            displaySeconds = seconds;
        }

        if (minutes === 0 && seconds === 0) {
            timerBox.innerHTML = '<b>00:00</b>';
            setTimeout(() => {
                clearInterval(timerInterval); // Use the variable to clear the interval
                alert('Time is over');
                sendData();
            }, 500);
        }
        console.log(displayMinutes, displaySeconds);
        timerBox.innerHTML = `<b>${displayMinutes}:${displaySeconds}</b>`;

    }, 1000);

};


$.ajax({
    type: 'GET',
    url: `${url}/data`, // Gets data from JsonResponse
    success: function(response) {
        const data = response.data;
        const time = response.time;
        data.forEach(element => { // A dictionary of a Question and its answers
            for (const [question, answers] of Object.entries(element)) {
                quizBox.innerHTML += `
                    <hr>
                    <div class="mb-2">
                        <b>${question}</b>
                    </div>
                `;
                answers.forEach(answer => {
                    quizBox.innerHTML += `
                        <div>
                            <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                            <label for="${question}">${answer}</label>
                        </div>
                    `;
                });
            }
        });
        activateTimer(time);
    },
    error: function(error) {
        console.log(error);
    }
});

const quizForm = document.getElementById('quiz-form');
const csrf = document.getElementsByName('csrfmiddlewaretoken');

const resultBox = document.getElementById('result-box');

const sendData = () => {
    clearInterval(timerInterval); // Stop the timer when sendData is called
    timerBox.remove();

    const elements = [...document.getElementsByClassName('ans')];
    const data = {};
    data['csrfmiddlewaretoken'] = csrf[0].value;
    elements.forEach(el => {
        if (el.checked) {
            data[el.name] = el.value;
        } else {
            if (!data[el.name]) {
                data[el.name] = null;
            }
        }
    });


    $.ajax({
        type: 'POST',
        url: `${url}/save`,
        data: data,
        success: function(response) {
            const results = response.results;

            quizForm.remove();

            results.forEach(res => {
                let resDiv = document.createElement('div');

                for (const [question, resp] of Object.entries(res)) {
                    resDiv.innerHTML += question;

                    const classes = ['container', 'p-3', 'text-light', 'h4'];
                    resDiv.classList.add(...classes);

                    if (resp == 'not answered') {
                        resDiv.innerHTML += ' — Not answered';
                        resDiv.classList.add('bg-danger');
                    } else {
                        const answer = resp['answered'];
                        const correct = resp['correct_answer'];

                        if (answer == correct) {
                            resDiv.classList.add('bg-success');
                            resDiv.innerHTML += ` Answered: ${answer}`;
                        } else {
                            resDiv.classList.add('bg-danger');
                            resDiv.innerHTML += `| Answered: ${answer}`;
                            resDiv.innerHTML += `| Correct answer: ${correct}`;
                        }
                    }
                }
                resultBox.append(resDiv);
            });
        },
        error: function(error) {
            console.log(error);
        }
    });
};


quizForm.addEventListener('submit', element => {
    element.preventDefault();

    sendData();
});