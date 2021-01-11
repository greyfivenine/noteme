$(document).ready(function() {
    document.querySelectorAll('.hide-button').forEach(
        item => item.addEventListener('click', function() {
            var block_id = '#' + $(this).attr('to')
            if ($(block_id).css('display').toLowerCase() == 'flex'){
                $(block_id).hide(300);
            }else{
                $(block_id).show(300);
            }
        })
    );

    $("button[name='button_delete']").click(function() {
        $.get('/notes/delete/', {note_id: $(this).attr('note_id')}, function(data){
            $('.content').html(data);
        });
    });
});
