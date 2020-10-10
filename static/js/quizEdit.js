quizForm = document.querySelector('.quizEdit-form');
quizContent = document.querySelector('.quizEdit-content');
editQuizBtn = document.querySelector('.quizEdit-btn');
cancelBtn = document.querySelector('.btnCancel');

editQuizBtn.addEventListener('click', () => {
    quizContent.classList.add('hide');
    quizForm.classList.remove('hide');
});

cancelBtn.addEventListener('click', () => {
    quizForm.classList.add('hide');
    quizContent.classList.remove('hide');
});