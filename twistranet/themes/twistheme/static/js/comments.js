var base_comment_message = '';

commentOnSubmit = function(comments_container) {
  var cform = jq('form', comments_container);
  var cUrl = cform.attr('action');
  cform.submit(function(e){
      e.preventDefault();
      e.stopPropagation();
      comments_container.waitLoading();
      // it could be more simple,
      // but take care to remove the 'redirect_to' var
      data = {
        redirect_to : '',
        description: jq("textarea[name='description']", cform).val(),
        csrfmiddlewaretoken : jq("input[name='csrfmiddlewaretoken']", cform).val()
      };
      jq.post(cUrl, data, function(html) {
          loadLastComment(comments_container, html);
          // TODO : debug this ...
          // the django form returns by default the request value
          // so we remove it
          new_cform = jq('form', comments_container);
          jq("textarea[name='description']", new_cform).val("");
      });
      return false;
  });
}

loadLastComment = function(comments_container, html) {
    comments_container.stopWaitLoading();
    jq('form:first', comments_container).before(html);
    window.setTimeout(function() {jq('.comment-description-field', comments_container).trigger('focusout')}, 3);
    twistranet.showCommentsActions();
    jq('a.confirmbefore', comments_container).click(function(e){
       e.preventDefault();
       initConfirmBox(this);
    } );
}

loadComments = function(ID, html) {
    comments_container = jq("#view_comments"+ID);
    comments_container.empty();
    comments_container.prepend(html);
    jq("#view"+ID).parent().css('visibility','hidden');
    twistranet.showCommentsActions();
    commentOnSubmit(comments_container);
    commentOnFocus(comments_container);
    jq('.comment-description-field', comments_container).focus();
    jq('a.confirmbefore', comments_container).click(function(e){
       e.preventDefault();
       initConfirmBox(this);
    } );
}

commentOnFocus = function(comments_container) {
    jq('.comment-description-field', comments_container).val(base_comment_message);
    jq('.comment-description-field', comments_container).focusin(function(){
        comment = jq(this).val();
        if (comment==base_comment_message) jq(this).val('');
        jq(this).addClass('comment-active');
        // add a small timeout to fix a bug under chrome
        window.setTimeout(function() {jq('input[type=submit]', comments_container).show()}, 3);
        
    });
    jq('.comment-description-field', comments_container).focusout(function(){
        comment = jq(this).val();
        if (!comment) {
            jq(this).removeClass('comment-active');
            jq(this).val(base_comment_message);
            jq('input[type=submit]', comments_container).hide();
        }
    });
    
}

jq(function() 
{
  jq(".view_comments").click(function() 
  {
    var ID = jq(this).attr("id");
    var comment_action = jq(this).parents('li');
    parent = jq(comment_action).parent();
    parent.waitLoading('left:-70px; top:-11px');
    jq.ajax({
      type: "GET",
      url: home_url + "comment/" + ID + "/list.xml",
      // data: "msg_id="+ ID, 
      cache: false,
      success: function(html){
        parent.stopWaitLoading();
        loadComments(ID, html);
        jq(comment_action).removeClass('add-comment').removeClass('view-all-comments');
      }
    });
    return false;
  })
  base_comment_message = jq('#commentmessage').text();
});

