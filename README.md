djang-superbulk
===============

Django app/view that adds the ability to execute many requests inside of a single HTTP connection

example usage:
 ```javascript
data = [{
  method:'GET',
uri:'/api/internal/v1/invoice/',
body:JSON.stringify({
  slug: '1231'
})}
]
```
