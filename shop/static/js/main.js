function deleteRequest (url){
    $.ajax({                            //$ = llama a Jquery.
        url : url,
        method : 'DELETE'
    });
}

