(function(){
  var LS={get:function(k){try{return localStorage.getItem(k);}catch(e){return null;}},set:function(k,v){try{localStorage.setItem(k,v);}catch(e){}}};
  function bind(f){
    f.addEventListener('submit',function(e){
      if(!window.fetch||!window.FormData)return; // fall back to a normal POST to Kit
      e.preventDefault();
      var note=f.querySelector('.formnote'),btn=f.querySelector('button[type=submit]'),email=f.querySelector('input[type=email]');
      btn.disabled=true;note.className='formnote';note.textContent='Subscribing…';
      fetch(f.action,{method:'POST',body:new FormData(f),headers:{'Accept':'application/json'}})
        .then(function(r){return r.json().catch(function(){return {};});})
        .then(function(d){
          if(d&&d.status==='success'){
            LS.set('hfd_subscribed','1');
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
  }
  Array.prototype.forEach.call(document.querySelectorAll('form[data-kit-form]'),bind);

  // Copy buttons on the Starter Prompts page
  Array.prototype.forEach.call(document.querySelectorAll('.copybtn[data-copy]'),function(b){
    b.addEventListener('click',function(){
      var c=document.querySelector('#'+b.getAttribute('data-copy')+' pre code');
      if(!c||!navigator.clipboard)return;
      navigator.clipboard.writeText(c.textContent).then(function(){b.textContent='Copied';setTimeout(function(){b.textContent='Copy prompt';},1500);});
    });
  });

  // Exit intent: guide and issue pages only, desktop only, once per browser, dismissible, never after a signup.
  var page=document.querySelector('main .guide, main .issue');
  if(!page||!window.matchMedia||!window.HTMLDialogElement)return;
  if(!window.matchMedia('(min-width: 900px) and (hover: hover) and (pointer: fine)').matches)return;
  if(LS.get('hfd_subscribed')||LS.get('hfd_exit_seen'))return;
  var armed=false,typed=false;
  setTimeout(function(){armed=true;},12000);
  document.addEventListener('focusin',function(e){if(e.target&&e.target.type==='email')typed=true;});
  function show(){
    if(!armed||typed||LS.get('hfd_exit_seen'))return;
    LS.set('hfd_exit_seen','1');
    document.removeEventListener('mouseout',onOut);
    var d=document.createElement('dialog');d.className='exitbox';d.setAttribute('aria-labelledby','exit-h');
    d.innerHTML='<button type="button" class="x" aria-label="Close">\u00d7</button>'+
      '<h2 id="exit-h">Before you go: '+'13'+' free Starter Prompts</h2>'+
      '<p>Plan-first, debugging and &quot;prove it&#x27;s done&quot; prompts for coding agents, vibe coding and game dev. Join Hotfix Daily (free, weekdays, about 3 minutes) and get them right away.</p>'+
      '<form class="signup" action="https://app.kit.com/forms/10075086/subscriptions" method="post" data-kit-form="10075086" data-redirect="/welcome/">'+
      '<label class="sr" for="email-exit">Email address</label>'+
      '<input id="email-exit" type="email" name="email_address" required autocomplete="email" inputmode="email" placeholder="you@example.com">'+
      '<button type="submit">Send me the prompts</button>'+
      '<p class="formnote" role="status" aria-live="polite">Free. Unsubscribe in one click. We won\u2019t show this again.</p></form>';
    document.body.appendChild(d);
    bind(d.querySelector('form'));
    d.querySelector('.x').addEventListener('click',function(){d.close();});
    d.addEventListener('click',function(e){if(e.target===d)d.close();});
    d.showModal();
  }
  function onOut(e){if(!e.relatedTarget&&e.clientY<=0)show();}
  document.addEventListener('mouseout',onOut);
})();
