function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const init = () => {

    const cards = document.querySelectorAll('.card')
    const question_detail = document.querySelector('.question_detail')
    const correct = document.querySelectorAll('.correct')
    if(cards) {
        for(const card of cards) {

            const LikeButton = card.querySelector('.LikeButton')
            const LikeCounter = card.querySelector('.LikeCount')
            const questionId = card.dataset.questionId
            const answerId = card.dataset.answerId
            let id = questionId ? questionId : answerId
            let url = answerId ? '/like_async_answer' : '/like_async'


            LikeButton.addEventListener('click', () => {
                const request = new Request(id + url, {
                    method: 'post',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        key: 'value',
                        key2: 'value2'
                    })
                })
                fetch(request)
                    .then((response) => response.json())
                    .then((data) => {
                        LikeCounter.value = data.likes_count
                    })

            })
        }
    }
    if(question_detail) {

        const LikeButton = question_detail.querySelector('.LikeButton')
        const LikeCounter = question_detail.querySelector('.LikeCount')
        const questionId = question_detail.dataset.questionId

        LikeButton.addEventListener('click', () => {
            const request = new Request(questionId + '/like_async', {
                method: 'post',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    key: 'value',
                    key2: 'value2'
                })
            })
            fetch(request)
                .then((response) => response.json())
                .then((data) => {
                    LikeCounter.value = data.likes_count
                })
        })
    }
    if(correct) {
        for(const correctCheckBox of correct) {
            const answerId = correctCheckBox.dataset.answerId
            correctCheckBox.addEventListener('click', () => {
                const request = new Request(answerId + '/correct_async', {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        key: 'value',
                        key2: 'value2'
                    })
                })
                fetch(request)
                    .then((response) => response.json())
                    .then((data) => {
                        correctCheckBox.value = data.correct
                    })
                })
            }
        }
}

init()