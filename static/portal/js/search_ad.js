/**
 * Created by vlva on 21.07.17.
 */
$(function(){
    $(".input-group-btn .dropdown-menu li a").click(function(){

        var selText = $(this).html();

        $(this).parents('.input-group-btn').find('.btn-search').html(selText);   });

    $(".input-group-btn .dropdown-menu li").click(function(){
        var selValue =  $(this).attr("value");

        $('.type_search').attr("value", selValue);
    });
});