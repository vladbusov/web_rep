

function setLike(id, is_like, is_question, callback) {
jQuery.ajax({
    url: '/app/like/',
    type: 'POST',

    data: {
        'id': id,
        'is_like': is_like,
        'is_questions': is_question
    },
    success: function (data) {
        if (data.status == 'ok') {
            console.log("OK");
            console.log(data);

            callback(data.answer.rating);
        } else {
            console.log(data)
        }
    },
    error: function () {
        console.log("error");
    }
})
}

$("#like").click(function (item) {
    var question_id = $(this).parent().parent().data().id;
    console.log(question_id);
    setLike(question_id, 'True', 'True', function (rating) {
        console.log(rating);
        $("#rating228").text(rating);
    })
});

