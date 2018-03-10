app.ready(function() {
    $('.search-input').bind("keypress",function(event){
        if(event.keyCode == "13") {
            var keyword = this.value;
            to_url = '/search/' + keyword + '/1';
            top.location.href = to_url;
        }
    });
});