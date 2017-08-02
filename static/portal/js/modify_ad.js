/**
 * Created by vlva on 01.08.17.
 */
/**
 * Created by vlva on 21.07.17.
 */
$(function(){
    $(".input-group-btn .dropdown-menu li a").click(function(){

        var sel_text = $(this).html();

        $(this).parents('.input-group-btn').find('.btn-search').html(sel_text);   });

    $(".input-group-btn .dropdown-menu li").click(function(){
        var sel_value =  $(this).attr("value");

        $('.type_search').attr("value", sel_value);
    });
});