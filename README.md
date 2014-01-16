django-superbulk
===============

Django app/view that adds the ability to execute many requests inside of a single HTTP connection.  django-superbulk is compatible with tastypie, django-REST or any other django based view system.

###WHY?
**Transactions! Transactions! Transactions!** The major reason is to be able to commit REST operations transactionally.  Tastypie allows bulk operations on a single resource, but not accross multiple resources. Superbulk inherits Djano's transactional operations.  All of the requests succed or they all fail (and roll back).

**Performance** is another issue.  While not generally critical some applications can benefit from this. Such as bulk write of a large number of items, or fetching diverse data on bootstrap from networked devices with a high lag time (mobile phones?).

###Security:
Django-superbulk passes on security to the views, where it is handled normally.  No request can be made using superbulk that the user can't make otherwise.

###IE8:
Older browsers don't support all of HTTP's new verbs (PATCH is not supported by IE8 and lower).  Since requests are wrapped in a POST request, this problem can be solved by using superbulk.

##example client:
* __data__ is sent as an array of objects, with three fields (always).
* __method__ is GET, POST, PATCH, UPDATE, DELETE, or any other HTTP verb you use.
* __uri__ is the absolute path (not including http and domain) to your django-view.
* __body__ is always a string, but may contain any data. Here it is a serialized JSON object.


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
	];

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
For the failfast version (Eg: 1000000 transactions, but it will stop after the first failed one)
```javascript

	data = { failfast: True,
            content: [{
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
           };

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


## Installing:

```
#TODO: Replace this with pip instructions when available in pipy
git clone git@github.com:thelonecabbage/django-superbulk.git
cd django-superbulk
python setup.py install

or another option would be to:

pip install git+https://github.com/thelonecabbage/django-superbulk.git
(Note the https form)
```

Add this url (or any other you prefer) to your urls.py file.
```python
   urlpatterns += patterns('django_superbulk'
      # this is the url for the more permissive
      # handling where some transactions may fail but this
      # returns a list with the results of the execution
      url(r'^api/superbulk/$', 'superbulk'),

      # this will handle all the post data as a single transaction
      url(r'^api/superbulk_transactional/$', 'superbulk-atomic'),

   )
```

##return result:
Errors in any of the items will result in the entire operation failing (Atomic Transactions).
Successfull returns return an array of objects in the same order and length submitted.
```javascript
[{
   status_code: 201,
   headers: {...},
   content: ''
},
{
   status_code: 201,
   headers: {...},
   content: ''
}]
```

Tests:
    In order to run the tests you will need nose and lettuce.

    They can be run with the usual:

    ```
        cd superbulk_test && python manage.py harvest
    ```

