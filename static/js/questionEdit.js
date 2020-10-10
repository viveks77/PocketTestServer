questionForm = document.querySelector('.questionEdit-form');
questionContent = document.querySelector('.questionEdit-titles');
editQuestionBtn = document.querySelector('.questionEdit-btn');


editQuestionBtn.addEventListener('click', () => {
    questionContent.classList.add('hide');
    questionForm.classList.remove('hide');
});
