$(document).ready(function(){
    // alert(Price_url);
    $.ajax({
        url: Price_url,
        success:function(data){
            console.log(data.prices);
            $.each(data.prices,function(key,value){
                $('[data-toggle="tooltip"]').tooltip();
                $('#silver_nav').html('$'+value.silver_price);
                $('#silver_nav').parent().attr('data-original-title','Last Updated: '+value.updated_at);
                $('#gold_nav').html('$'+value.gold_price);
                $('#gold_nav').parent().attr('data-original-title','Last Updated: '+value.updated_at);
                $('#platinum_nav').html('$'+value.platinum_price);
                $('#platinum_nav').parent().attr('data-original-title','Last Updated: '+value.updated_at);
                $('#palladium_nav').html('$'+value.palladium_price);
                $('#palladium_nav').parent().attr('data-original-title','Last Updated: '+value.updated_at);
            });
        }
    });
});