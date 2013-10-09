djang-superbulk
===============

Django app/view that adds the ability to execute many requests inside of a single HTTP connection

##example client:
* "__data__" is sent as an array of objects, with three fields (always).  
* "__method__" is GET, POST, PATCH, UPDATE, DELETE, or any other HTTP verb you use.  
* "__uri__" is the absolute path (not including http and domain) to your django-view.  
* "__body__" is always a string, but can contain any data, as here a serialized JSON object.

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
