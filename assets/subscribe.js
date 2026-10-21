(function(){
  var forms=document.querySelectorAll('form[data-kit-form]');
  Array.prototype.forEach.call(forms,function(f){
    f.addEventListener('submit',function(e){
      if(!window.fetch||!window.FormData)return; // fall back to a normal POST to Kit
      e.preventDefault();
      var note=f.querySelector('.formnote'),btn=f.querySelector('button'),email=f.querySelector('input[type=email]');
      btn.disabled=true;note.className='formnote';note.textContent='Subscribing…';
      fetch(f.action,{method:'POST',body:new FormData(f),headers:{'Accept':'application/json'}})
        .then(function(r){return r.json().catch(function(){return {};});})
        .then(function(d){
          if(d&&d.status==='success'){
            note.className='formnote ok';
            note.textContent='You\u2019re in! Check your inbox (and Promotions tab) to confirm your subscription.';
            email.value='';
            var to=f.getAttribute('data-redirect');
            if(to){setTimeout(function(){window.location.href=to;},600);}
          }else{
            var msg=(d&&d.errors&&d.errors.messages&&d.errors.messages[0])||'Something went wrong. Please try again.';
            note.className='formnote err';note.textContent=msg;
          }
        })
        .catch(function(){f.submit();})
        .then(function(){btn.disabled=false;});
    });
  });
})();
