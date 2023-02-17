#### About
Here is documented the changes required for RESQL and POSTGRES DB database connection


`application.yml`  
```
spring:
  profiles:
    active: dev

server:
  port: 8082

headers:
  contentSecurityPolicy: "script-src 'self'"

userIPHeaderName: x-forwarded-for
#append a whitespace character at the end of prefix (before newline) if you want it to be separate from main message body
userIPLoggingPrefix: from IP
userIPLoggingMDCkey: userIP

h2:
  console:
    enabled: true

sqlms:
  saved-queries-dir: "./templates/"
  datasources:
    - name: templates
      jdbcUrl: jdbc:postgresql://USERS-DB:5433/DBPLACEHOLDER?user=USERPLACEHOLDER&password=PASSPLACEHOLDER&ssl=true";
      username: USERPLACEHOLDER
      password: PASSPLACEHOLDER
      driverClassname: org.postgresql.Driver
logging:
  level:
    root: info
```
