djang-superbulk
===============

Django app/view that adds the ability to execute many requests inside of a single HTTP connection

example usage:
 ```javascript
data = [{
   method:'POST',
   uri:'/api/v1/customer/',
   body:JSON.stringify({
      id: 'asdf-asdf-asdf-sadf',
      name: 'Justin'
      })
   },{
   method:'POST',
   uri:'/api/v1/invoice/',
   body:JSON.stringify({
      customer_id: 'asdf-asdf-asdf-sadf',
      invoice_no: '0001'
      })
   }
]

$.ajax({
   url: '/api/superbulk/',
   dataType: "application/json",
   data: JSON.stringify(data),
   type:'POST',
   contentType:'application/json',
   headers: {
      'X-CSRFToken': (document.cookie.match(/csrftoken=([0-9a-zA-Z]*)/) || ['']).pop()
   }
});
```
