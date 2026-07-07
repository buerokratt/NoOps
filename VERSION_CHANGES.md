# Version Change History

## Change on 2025-11-27 08:59:37 (EET)
**Author:** Varmo <101868197+varmoh@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index 1c27dd8..e38536c 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -14,7 +14,7 @@ All application version numbers listed here represent the latest available **rel
 | Resql               | vX.X.X         | YYYY-MM-DD   |
 | S3Ferry             | vX.X.X         | YYYY-MM-DD   |
 | S3Ferry-publish     | vX.X.X         | YYYY-MM-DD   |
-| TIM                 | vX.X.X         | YYYY-MM-DD   |
+| TIM                 | v2.3.6         | 2025-11-25   |
 | UsersDB             | vX.X.X         | YYYY-MM-DD   |
 | TimDB               | vX.X.X         | YYYY-MM-DD   |
 | XTR                 | vX.X.X         | YYYY-MM-DD   |
```

## Change on 2025-11-27 11:17:41 (EET)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index e38536c..b174299 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -7,25 +7,25 @@ All application version numbers listed here represent the latest available **rel
 
 | Application         | Latest Version | Release Date |
 |---------------------|----------------|--------------|
-| CronManager         | vX.X.X         | YYYY-MM-DD   |
+| CronManager         | v1.1.23        | 2025-11-25   |
 | Ruuter              | v2.2.8         | 2025-11-25   |
 | Ruuter-Private      | v2.2.8         | 2025-11-25   |
-| DataMapper          | vX.X.X         | YYYY-MM-DD   |
-| Resql               | vX.X.X         | YYYY-MM-DD   |
-| S3Ferry             | vX.X.X         | YYYY-MM-DD   |
-| S3Ferry-publish     | vX.X.X         | YYYY-MM-DD   |
+| DataMapper          | v2.2.23        | 2025-11-25   |
+| Resql               | v1.3.5         | 2025-11-25   |
+| S3Ferry             | pre-alpha-1.1.1| 2025-11-25   |
+| S3Ferry-publish     | pre-alpha-1.1.1| 2025-11-25   |
 | TIM                 | v2.3.6         | 2025-11-25   |
-| UsersDB             | vX.X.X         | YYYY-MM-DD   |
-| TimDB               | vX.X.X         | YYYY-MM-DD   |
-| XTR                 | vX.X.X         | YYYY-MM-DD   |
-| NotificationsNode   | vX.X.X         | YYYY-MM-DD   |
-| OpenSearch          | vX.X.X         | YYYY-MM-DD   |
-| AuthLayer           | vX.X.X         | YYYY-MM-DD   |
-| backoffice          | vX.X.X         | YYYY-MM-DD   |
-| analytics           | vX.X.X         | YYYY-MM-DD   |
-| training            | vX.X.X         | YYYY-MM-DD   |
-| service             | vX.X.X         | YYYY-MM-DD   |
-| widget              | vX.X.X         | YYYY-MM-DD   |
+| UsersDB             | postgres:14.1  | 2025-11-25   |
+| TimDB               | postgres:14.1  | 2025-11-25   |
+| XTR                 | pre-alpha-test-1.1.3| 2025-11-25   |
+| NotificationsNode   | v2.1.61-notification-node| 2025-11-25   |
+| OpenSearch          | 1.3.16         | 2025-11-25   |
+| AuthLayer           | v1.1.1         | 2025-11-25   |
+| backoffice          | v2.1.61        | 2025-11-25   |
+| analytics           | v1.1.33        | 2025-11-25   |
+| training            | v2.1.34        | 2025-11-25   |
+| service             | temp-fix-1.1.2-temp| 2025-11-25   |
+| widget              | v2.1.37        | 2025-11-25   |
 
 
 ---
```

## Change on 2025-12-02 14:01:31 (EET)
**Author:** KlviG <78801020+KlviG@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index b174299..fac56da 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -7,26 +7,25 @@ All application version numbers listed here represent the latest available **rel
 
 | Application         | Latest Version | Release Date |
 |---------------------|----------------|--------------|
-| CronManager         | v1.1.23        | 2025-11-25   |
 | Ruuter              | v2.2.8         | 2025-11-25   |
 | Ruuter-Private      | v2.2.8         | 2025-11-25   |
-| DataMapper          | v2.2.23        | 2025-11-25   |
 | Resql               | v1.3.5         | 2025-11-25   |
-| S3Ferry             | pre-alpha-1.1.1| 2025-11-25   |
-| S3Ferry-publish     | pre-alpha-1.1.1| 2025-11-25   |
 | TIM                 | v2.3.6         | 2025-11-25   |
-| UsersDB             | postgres:14.1  | 2025-11-25   |
-| TimDB               | postgres:14.1  | 2025-11-25   |
-| XTR                 | pre-alpha-test-1.1.3| 2025-11-25   |
+| CronManager         | v1.1.28        | 2025-11-25   |
+| DataMapper          | v2.2.23        | 2025-11-25   |
 | NotificationsNode   | v2.1.61-notification-node| 2025-11-25   |
 | OpenSearch          | 1.3.16         | 2025-11-25   |
-| AuthLayer           | v1.1.1         | 2025-11-25   |
+| S3Ferry             | pre-alpha-1.1.1| 2025-11-25   |
+| S3Ferry-publish     | pre-alpha-1.1.1| 2025-11-25   |
+| XTR                 | pre-alpha-test-1.1.3| 2025-11-25   |
+| widget              | v2.1.37        | 2025-11-25   |
 | backoffice          | v2.1.61        | 2025-11-25   |
 | analytics           | v1.1.33        | 2025-11-25   |
 | training            | v2.1.34        | 2025-11-25   |
 | service             | temp-fix-1.1.2-temp| 2025-11-25   |
-| widget              | v2.1.37        | 2025-11-25   |
-
+| AuthLayer           | v1.1.1         | 2025-11-25   |
+| UsersDB             | postgres:14.1  | 2025-11-25   |
+| TimDB               | postgres:14.1  | 2025-11-25   |
 
 ---
 
```

## Change on 2025-12-10 12:15:45 (EET)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index fac56da..d9f3307 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -18,7 +18,7 @@ All application version numbers listed here represent the latest available **rel
 | S3Ferry             | pre-alpha-1.1.1| 2025-11-25   |
 | S3Ferry-publish     | pre-alpha-1.1.1| 2025-11-25   |
 | XTR                 | pre-alpha-test-1.1.3| 2025-11-25   |
-| widget              | v2.1.37        | 2025-11-25   |
+| widget              | v2.1.53        | 2025-12-9   |
 | backoffice          | v2.1.61        | 2025-11-25   |
 | analytics           | v1.1.33        | 2025-11-25   |
 | training            | v2.1.34        | 2025-11-25   |
@@ -26,7 +26,10 @@ All application version numbers listed here represent the latest available **rel
 | AuthLayer           | v1.1.1         | 2025-11-25   |
 | UsersDB             | postgres:14.1  | 2025-11-25   |
 | TimDB               | postgres:14.1  | 2025-11-25   |
-
+| Backoffice DSL                 | backoffice-module-test-1.6.19  | 2025-11-25   |
+| Analytics DSL                 | analytics-module-test-1.6.11  | 2025-11-25   |
+| Training DSL                 | training-module-test-1.6.4  | 2025-11-25   |
+| Service DSL                 | service-module-test-1.5.30  | 2025-11-25   |
 ---
 
 ## Versioning Notes
```

## Change on 2025-12-16 15:42:47 (EET)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index d9f3307..2b2f388 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -11,7 +11,7 @@ All application version numbers listed here represent the latest available **rel
 | Ruuter-Private      | v2.2.8         | 2025-11-25   |
 | Resql               | v1.3.5         | 2025-11-25   |
 | TIM                 | v2.3.6         | 2025-11-25   |
-| CronManager         | v1.1.28        | 2025-11-25   |
+| CronManager         | prod-3.0.1     | 2025-12-16   |
 | DataMapper          | v2.2.23        | 2025-11-25   |
 | NotificationsNode   | v2.1.61-notification-node| 2025-11-25   |
 | OpenSearch          | 1.3.16         | 2025-11-25   |
```

## Change on 2026-01-13 12:48:49 (EET)
**Author:** Varmo <101868197+varmoh@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index 2b2f388..200a5f7 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -2,9 +2,43 @@
 
 All application version numbers listed here represent the latest available **release versions** intended for deployment.
 
+
+
+Upcoming version - **V3.1.0**
+---
+
+| Application         | Latest Version | Release Date |
+|---------------------|----------------|--------------|
+| Ruuter              | v2.2.8         | 2025-11-25   |
+| Ruuter-Private      | v2.2.8         | 2025-11-25   |
+| Resql               | v1.3.5         | 2025-11-25   |
+| TIM                 | v2.3.6         | 2025-11-25   |
+| CronManager         | prod-3.0.1     | 2025-12-16   |
+| DataMapper          | v2.2.28        | 2025-11-25   |
+| NotificationsNode   | v2.1.61-notification-node| 2026-01-13   |
+| OpenSearch          | 1.3.16         | 2025-11-25   |
+| S3Ferry             | pre-alpha-1.1.1| 2025-11-25   |
+| S3Ferry-publish     | pre-alpha-1.1.1| 2025-11-25   |
+| XTR                 | pre-alpha-test-1.1.3| 2025-11-25   |
+| widget              | v2.1.53        | 2025-12-9   |
+| backoffice          | v2.1.61        | 2025-11-25   |
+| analytics           | v1.1.33        | 2025-11-25   |
+| training            | v2.1.34        | 2025-11-25   |
+| service             | temp-fix-1.1.2-temp| 2025-11-25   |
+| AuthLayer           | v1.1.1         | 2025-11-25   |
+| UsersDB             | postgres:14.1  | 2025-11-25   |
+| TimDB               | postgres:14.1  | 2025-11-25   |
+| Backoffice DSL                 | backoffice-module-test-1.6.19  | 2025-11-25   |
+| Analytics DSL                 | analytics-module-test-1.6.11  | 2025-11-25   |
+| Training DSL                 | training-module-test-1.6.4  | 2025-11-25   |
+| Service DSL                 | service-module-test-1.5.30  | 2025-11-25   |
 ---
 
 
+---
+Current version - V3.0.1
+---
+
 | Application         | Latest Version | Release Date |
 |---------------------|----------------|--------------|
 | Ruuter              | v2.2.8         | 2025-11-25   |
```

## Change on 2026-01-13 12:49:48 (EET)
**Author:** Varmo <101868197+varmoh@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index 200a5f7..94a202d 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -14,8 +14,8 @@ Upcoming version - **V3.1.0**
 | Resql               | v1.3.5         | 2025-11-25   |
 | TIM                 | v2.3.6         | 2025-11-25   |
 | CronManager         | prod-3.0.1     | 2025-12-16   |
-| DataMapper          | v2.2.28        | 2025-11-25   |
-| NotificationsNode   | v2.1.61-notification-node| 2026-01-13   |
+| DataMapper          | v2.2.28        | 2025-01-13   |
+| NotificationsNode   | v2.1.61-notification-node| 2026-11-25   |
 | OpenSearch          | 1.3.16         | 2025-11-25   |
 | S3Ferry             | pre-alpha-1.1.1| 2025-11-25   |
 | S3Ferry-publish     | pre-alpha-1.1.1| 2025-11-25   |
```

## Change on 2026-01-13 13:20:58 (EET)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index 94a202d..817db1c 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -9,29 +9,29 @@ Upcoming version - **V3.1.0**
 
 | Application         | Latest Version | Release Date |
 |---------------------|----------------|--------------|
-| Ruuter              | v2.2.8         | 2025-11-25   |
-| Ruuter-Private      | v2.2.8         | 2025-11-25   |
-| Resql               | v1.3.5         | 2025-11-25   |
-| TIM                 | v2.3.6         | 2025-11-25   |
-| CronManager         | prod-3.0.1     | 2025-12-16   |
-| DataMapper          | v2.2.28        | 2025-01-13   |
-| NotificationsNode   | v2.1.61-notification-node| 2026-11-25   |
-| OpenSearch          | 1.3.16         | 2025-11-25   |
-| S3Ferry             | pre-alpha-1.1.1| 2025-11-25   |
-| S3Ferry-publish     | pre-alpha-1.1.1| 2025-11-25   |
-| XTR                 | pre-alpha-test-1.1.3| 2025-11-25   |
-| widget              | v2.1.53        | 2025-12-9   |
-| backoffice          | v2.1.61        | 2025-11-25   |
-| analytics           | v1.1.33        | 2025-11-25   |
-| training            | v2.1.34        | 2025-11-25   |
-| service             | temp-fix-1.1.2-temp| 2025-11-25   |
-| AuthLayer           | v1.1.1         | 2025-11-25   |
-| UsersDB             | postgres:14.1  | 2025-11-25   |
-| TimDB               | postgres:14.1  | 2025-11-25   |
-| Backoffice DSL                 | backoffice-module-test-1.6.19  | 2025-11-25   |
-| Analytics DSL                 | analytics-module-test-1.6.11  | 2025-11-25   |
-| Training DSL                 | training-module-test-1.6.4  | 2025-11-25   |
-| Service DSL                 | service-module-test-1.5.30  | 2025-11-25   |
+| Ruuter              | v2.2.8         | 2026-01-13   |
+| Ruuter-Private      | v2.2.8         | 2026-01-13   |
+| Resql               | v1.3.5         | 2026-01-13   |
+| TIM                 | v2.3.6         | 2026-01-13   |
+| CronManager         | v1.1.33        | 2026-01-13   |
+| DataMapper          | v2.2.28        | 2026-01-13   |
+| NotificationsNode   | v2.1.79-notification-node| 2026-01-13   |
+| OpenSearch          | 1.3.16         | 2026-01-13   |
+| S3Ferry             | pre-alpha-1.1.1| 2026-01-13   |
+| S3Ferry-publish     | pre-alpha-1.1.1| 2026-01-13   |
+| XTR                 | pre-alpha-test-1.1.3| 2026-01-13   |
+| widget              | v2.1.58        | 2026-01-13   |
+| backoffice          | v2.1.79        | 2026-01-13   |
+| analytics           | v1.1.38        | 2026-01-13   |
+| training            | v2.1.40        | 2026-01-13   |
+| service             | v1.1.44        | 2026-01-13   |
+| AuthLayer           | v1.1.2         | 2026-01-13   |
+| UsersDB             | postgres:14.1  | 2026-01-13   |
+| TimDB               | postgres:14.1  | 2026-01-13   |
+| Backoffice DSL                 | backoffice-module-test-1.6.44  | 2026-01-13   |
+| Analytics DSL                 | analytics-module-test-1.6.14  | 2026-01-13   |
+| Training DSL                 | training-module-test-1.6.7  | 2026-01-13   |
+| Service DSL                 | service-module-test-1.6.3  | 2026-01-13   |
 ---
 
 
```

## Change on 2026-01-13 16:09:35 (EET)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index 817db1c..b7998d6 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -28,7 +28,7 @@ Upcoming version - **V3.1.0**
 | AuthLayer           | v1.1.2         | 2026-01-13   |
 | UsersDB             | postgres:14.1  | 2026-01-13   |
 | TimDB               | postgres:14.1  | 2026-01-13   |
-| Backoffice DSL                 | backoffice-module-test-1.6.44  | 2026-01-13   |
+| Backoffice DSL                 | backoffice-module-test-1.6.45  | 2026-01-13   |
 | Analytics DSL                 | analytics-module-test-1.6.14  | 2026-01-13   |
 | Training DSL                 | training-module-test-1.6.7  | 2026-01-13   |
 | Service DSL                 | service-module-test-1.6.3  | 2026-01-13   |
```

## Change on 2026-01-13 17:18:07 (EET)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index b7998d6..2460701 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -14,7 +14,7 @@ Upcoming version - **V3.1.0**
 | Resql               | v1.3.5         | 2026-01-13   |
 | TIM                 | v2.3.6         | 2026-01-13   |
 | CronManager         | v1.1.33        | 2026-01-13   |
-| DataMapper          | v2.2.28        | 2026-01-13   |
+| DataMapper          | v2.2.29        | 2026-01-13   |
 | NotificationsNode   | v2.1.79-notification-node| 2026-01-13   |
 | OpenSearch          | 1.3.16         | 2026-01-13   |
 | S3Ferry             | pre-alpha-1.1.1| 2026-01-13   |
```

## Change on 2026-01-19 11:55:47 (EET)
**Author:** Varmo <101868197+varmoh@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index 2460701..b92effa 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -14,13 +14,13 @@ Upcoming version - **V3.1.0**
 | Resql               | v1.3.5         | 2026-01-13   |
 | TIM                 | v2.3.6         | 2026-01-13   |
 | CronManager         | v1.1.33        | 2026-01-13   |
-| DataMapper          | v2.2.29        | 2026-01-13   |
+| DataMapper          | v2.2.30        | 2026-01-13   |
 | NotificationsNode   | v2.1.79-notification-node| 2026-01-13   |
 | OpenSearch          | 1.3.16         | 2026-01-13   |
 | S3Ferry             | pre-alpha-1.1.1| 2026-01-13   |
 | S3Ferry-publish     | pre-alpha-1.1.1| 2026-01-13   |
 | XTR                 | pre-alpha-test-1.1.3| 2026-01-13   |
-| widget              | v2.1.58        | 2026-01-13   |
+| widget              | downloadtemp-1.1.1        | 2026-01-13   |
 | backoffice          | v2.1.79        | 2026-01-13   |
 | analytics           | v1.1.38        | 2026-01-13   |
 | training            | v2.1.40        | 2026-01-13   |
```

## Change on 2026-01-20 13:32:23 (EET)
**Author:** Varmo <101868197+varmoh@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index b92effa..fe6d29f 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -14,13 +14,13 @@ Upcoming version - **V3.1.0**
 | Resql               | v1.3.5         | 2026-01-13   |
 | TIM                 | v2.3.6         | 2026-01-13   |
 | CronManager         | v1.1.33        | 2026-01-13   |
-| DataMapper          | v2.2.30        | 2026-01-13   |
+| DataMapper          | v2.2.31        | 2026-01-13   |
 | NotificationsNode   | v2.1.79-notification-node| 2026-01-13   |
 | OpenSearch          | 1.3.16         | 2026-01-13   |
 | S3Ferry             | pre-alpha-1.1.1| 2026-01-13   |
 | S3Ferry-publish     | pre-alpha-1.1.1| 2026-01-13   |
 | XTR                 | pre-alpha-test-1.1.3| 2026-01-13   |
-| widget              | downloadtemp-1.1.1        | 2026-01-13   |
+| widget              | v2.1.59        | 2026-01-13   |
 | backoffice          | v2.1.79        | 2026-01-13   |
 | analytics           | v1.1.38        | 2026-01-13   |
 | training            | v2.1.40        | 2026-01-13   |
```

## Change on 2026-01-21 16:12:18 (EET)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index fe6d29f..68834a8 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -28,7 +28,7 @@ Upcoming version - **V3.1.0**
 | AuthLayer           | v1.1.2         | 2026-01-13   |
 | UsersDB             | postgres:14.1  | 2026-01-13   |
 | TimDB               | postgres:14.1  | 2026-01-13   |
-| Backoffice DSL                 | backoffice-module-test-1.6.45  | 2026-01-13   |
+| Backoffice DSL                 | backoffice-module-test-3.1.4-stage  | 2026-01-13   |
 | Analytics DSL                 | analytics-module-test-1.6.14  | 2026-01-13   |
 | Training DSL                 | training-module-test-1.6.7  | 2026-01-13   |
 | Service DSL                 | service-module-test-1.6.3  | 2026-01-13   |
```

## Change on 2026-01-26 10:59:56 (EET)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index 024af1e..631eab3 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -28,7 +28,7 @@ Upcoming version - **V3.1.0**
 | AuthLayer           | v1.1.2         | 2026-01-13   |
 | UsersDB             | postgres:14.1  | 2026-01-13   |
 | TimDB               | postgres:14.1  | 2026-01-13   |
-| Backoffice DSL                 | backoffice-module-test-3.1.4-stage  | 2026-01-21   |
+| Backoffice DSL                 | backoffice-module-test-3.1.5-stage  | 2026-01-21   |
 | Analytics DSL                 | analytics-module-test-1.6.14  | 2026-01-13   |
 | Training DSL                 | training-module-test-1.6.7  | 2026-01-13   |
 | Service DSL                 | service-module-test-1.6.3  | 2026-01-13   |
```

## Change on 2026-01-26 11:00:39 (EET)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index 631eab3..89df971 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -13,7 +13,7 @@ Upcoming version - **V3.1.0**
 | Ruuter-Private      | v2.2.8         | 2026-01-13   |
 | Resql               | v1.3.5         | 2026-01-13   |
 | TIM                 | v2.3.6         | 2026-01-13   |
-| CronManager         | v1.1.33        | 2026-01-13   |
+| CronManager         | v1.1.40        | 2026-01-26   |
 | DataMapper          | v2.2.31        | 2026-01-13   |
 | NotificationsNode   | v2.1.79-notification-node| 2026-01-13   |
 | OpenSearch          | 1.3.16         | 2026-01-13   |
@@ -28,7 +28,7 @@ Upcoming version - **V3.1.0**
 | AuthLayer           | v1.1.2         | 2026-01-13   |
 | UsersDB             | postgres:14.1  | 2026-01-13   |
 | TimDB               | postgres:14.1  | 2026-01-13   |
-| Backoffice DSL                 | backoffice-module-test-3.1.5-stage  | 2026-01-21   |
+| Backoffice DSL                 | backoffice-module-test-3.1.5-stage  | 2026-01-26   |
 | Analytics DSL                 | analytics-module-test-1.6.14  | 2026-01-13   |
 | Training DSL                 | training-module-test-1.6.7  | 2026-01-13   |
 | Service DSL                 | service-module-test-1.6.3  | 2026-01-13   |
```

## Change on 2026-01-26 11:55:16 (EET)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index 89df971..785f24f 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -28,7 +28,7 @@ Upcoming version - **V3.1.0**
 | AuthLayer           | v1.1.2         | 2026-01-13   |
 | UsersDB             | postgres:14.1  | 2026-01-13   |
 | TimDB               | postgres:14.1  | 2026-01-13   |
-| Backoffice DSL                 | backoffice-module-test-3.1.5-stage  | 2026-01-26   |
+| Backoffice DSL                 | backoffice-module-test-3.1.4-stage  | 2026-01-26   |
 | Analytics DSL                 | analytics-module-test-1.6.14  | 2026-01-13   |
 | Training DSL                 | training-module-test-1.6.7  | 2026-01-13   |
 | Service DSL                 | service-module-test-1.6.3  | 2026-01-13   |
```

## Change on 2026-01-26 12:21:19 (EET)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index 785f24f..3028e60 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -28,7 +28,7 @@ Upcoming version - **V3.1.0**
 | AuthLayer           | v1.1.2         | 2026-01-13   |
 | UsersDB             | postgres:14.1  | 2026-01-13   |
 | TimDB               | postgres:14.1  | 2026-01-13   |
-| Backoffice DSL                 | backoffice-module-test-3.1.4-stage  | 2026-01-26   |
+| Backoffice DSL                 | backoffice-module-test-3.1.6-stage  | 2026-01-26   |
 | Analytics DSL                 | analytics-module-test-1.6.14  | 2026-01-13   |
 | Training DSL                 | training-module-test-1.6.7  | 2026-01-13   |
 | Service DSL                 | service-module-test-1.6.3  | 2026-01-13   |
```

## Change on 2026-01-26 12:35:11 (EET)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index 3028e60..feb32dd 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -28,7 +28,7 @@ Upcoming version - **V3.1.0**
 | AuthLayer           | v1.1.2         | 2026-01-13   |
 | UsersDB             | postgres:14.1  | 2026-01-13   |
 | TimDB               | postgres:14.1  | 2026-01-13   |
-| Backoffice DSL                 | backoffice-module-test-3.1.6-stage  | 2026-01-26   |
+| Backoffice DSL                 | backoffice-module-test-3.1.7-stage  | 2026-01-26   |
 | Analytics DSL                 | analytics-module-test-1.6.14  | 2026-01-13   |
 | Training DSL                 | training-module-test-1.6.7  | 2026-01-13   |
 | Service DSL                 | service-module-test-1.6.3  | 2026-01-13   |
```

## Change on 2026-01-28 12:06:52 (EET)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index feb32dd..8caca90 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -20,7 +20,7 @@ Upcoming version - **V3.1.0**
 | S3Ferry             | pre-alpha-1.1.1| 2026-01-13   |
 | S3Ferry-publish     | pre-alpha-1.1.1| 2026-01-13   |
 | XTR                 | pre-alpha-test-1.1.3| 2026-01-13   |
-| widget              | v2.1.59        | 2026-01-13   |
+| widget              | v2.1.61        | 2026-01-28   |
 | backoffice          | v2.1.79        | 2026-01-13   |
 | analytics           | v1.1.38        | 2026-01-13   |
 | training            | v2.1.40        | 2026-01-13   |
```

## Change on 2026-01-28 13:27:25 (EET)
**Author:** KlviG <78801020+KlviG@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index 8caca90..f945e51 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -4,7 +4,7 @@ All application version numbers listed here represent the latest available **rel
 
 
 
-Upcoming version - **V3.1.0**
+Upcoming version - **V3.1.1**
 ---
 
 | Application         | Latest Version | Release Date |
```

## Change on 2026-02-23 10:25:39 (EET)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index f945e51..9558ce0 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -13,25 +13,25 @@ Upcoming version - **V3.1.1**
 | Ruuter-Private      | v2.2.8         | 2026-01-13   |
 | Resql               | v1.3.5         | 2026-01-13   |
 | TIM                 | v2.3.6         | 2026-01-13   |
-| CronManager         | v1.1.40        | 2026-01-26   |
-| DataMapper          | v2.2.31        | 2026-01-13   |
-| NotificationsNode   | v2.1.79-notification-node| 2026-01-13   |
+| CronManager         | v1.1.41        | 2026-02-23   |
+| DataMapper          | v2.2.37        | 2026-02-23   |
+| NotificationsNode   | v2.1.92-notification-node| 2026-02-23   |
 | OpenSearch          | 1.3.16         | 2026-01-13   |
 | S3Ferry             | pre-alpha-1.1.1| 2026-01-13   |
 | S3Ferry-publish     | pre-alpha-1.1.1| 2026-01-13   |
 | XTR                 | pre-alpha-test-1.1.3| 2026-01-13   |
-| widget              | v2.1.61        | 2026-01-28   |
-| backoffice          | v2.1.79        | 2026-01-13   |
-| analytics           | v1.1.38        | 2026-01-13   |
-| training            | v2.1.40        | 2026-01-13   |
-| service             | v1.1.44        | 2026-01-13   |
+| widget              | v2.1.69        | 2026-02-23   |
+| backoffice          | v2.1.98        | 2026-02-23   |
+| analytics           | v1.1.48        | 2026-02-23   |
+| training            | v2.1.47        | 2026-02-23   |
+| service             | v1.1.53        | 2026-02-23   |
 | AuthLayer           | v1.1.2         | 2026-01-13   |
 | UsersDB             | postgres:14.1  | 2026-01-13   |
 | TimDB               | postgres:14.1  | 2026-01-13   |
-| Backoffice DSL                 | backoffice-module-test-3.1.7-stage  | 2026-01-26   |
-| Analytics DSL                 | analytics-module-test-1.6.14  | 2026-01-13   |
-| Training DSL                 | training-module-test-1.6.7  | 2026-01-13   |
-| Service DSL                 | service-module-test-1.6.3  | 2026-01-13   |
+| Backoffice DSL                 | backoffice-module-test-3.2.18  | 2026-02-23   |
+| Analytics DSL                 | analytics-module-test-3.2.13  | 2026-02-23   |
+| Training DSL                 | training-module-test-3.2.9  | 2026-02-23   |
+| Service DSL                 | service-module-test-3.2.7  | 2026-02-23   |
 ---
 
 
```

## Change on 2026-02-23 10:46:46 (EET)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index 9558ce0..3a86893 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -4,7 +4,7 @@ All application version numbers listed here represent the latest available **rel
 
 
 
-Upcoming version - **V3.1.1**
+Upcoming version - **V3.2.0**
 ---
 
 | Application         | Latest Version | Release Date |
```

## Change on 2026-02-23 11:37:12 (EET)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index 3a86893..b452918 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -36,34 +36,34 @@ Upcoming version - **V3.2.0**
 
 
 ---
-Current version - V3.0.1
+Current version - V3.1.1
 ---
 
 | Application         | Latest Version | Release Date |
 |---------------------|----------------|--------------|
-| Ruuter              | v2.2.8         | 2025-11-25   |
-| Ruuter-Private      | v2.2.8         | 2025-11-25   |
-| Resql               | v1.3.5         | 2025-11-25   |
-| TIM                 | v2.3.6         | 2025-11-25   |
-| CronManager         | prod-3.0.1     | 2025-12-16   |
-| DataMapper          | v2.2.23        | 2025-11-25   |
-| NotificationsNode   | v2.1.61-notification-node| 2025-11-25   |
-| OpenSearch          | 1.3.16         | 2025-11-25   |
-| S3Ferry             | pre-alpha-1.1.1| 2025-11-25   |
-| S3Ferry-publish     | pre-alpha-1.1.1| 2025-11-25   |
-| XTR                 | pre-alpha-test-1.1.3| 2025-11-25   |
-| widget              | v2.1.53        | 2025-12-9   |
-| backoffice          | v2.1.61        | 2025-11-25   |
-| analytics           | v1.1.33        | 2025-11-25   |
-| training            | v2.1.34        | 2025-11-25   |
-| service             | temp-fix-1.1.2-temp| 2025-11-25   |
-| AuthLayer           | v1.1.1         | 2025-11-25   |
-| UsersDB             | postgres:14.1  | 2025-11-25   |
-| TimDB               | postgres:14.1  | 2025-11-25   |
-| Backoffice DSL                 | backoffice-module-test-1.6.19  | 2025-11-25   |
-| Analytics DSL                 | analytics-module-test-1.6.11  | 2025-11-25   |
-| Training DSL                 | training-module-test-1.6.4  | 2025-11-25   |
-| Service DSL                 | service-module-test-1.5.30  | 2025-11-25   |
+| Ruuter              | v2.2.8         | 2026-01-13   |
+| Ruuter-Private      | v2.2.8         | 2026-01-13   |
+| Resql               | v1.3.5         | 2026-01-13   |
+| TIM                 | v2.3.6         | 2026-01-13   |
+| CronManager         | v1.1.40        | 2026-01-13   |
+| DataMapper          | v2.2.31        | 2026-01-13   |
+| NotificationsNode   | v2.1.79-notification-node| 2026-01-13   |
+| OpenSearch          | 1.3.16         | 2026-01-13   |
+| S3Ferry             | pre-alpha-1.1.1| 2026-01-13   |
+| S3Ferry-publish     | pre-alpha-1.1.1| 2026-01-13   |
+| XTR                 | pre-alpha-test-1.1.3| 2026-01-13   |
+| widget              | v2.1.61        | 2026-01-13   |
+| backoffice          | v2.1.79        | 2026-01-13   |
+| analytics           | v1.1.38        | 2026-01-13   |
+| training            | v2.1.40        | 2026-01-13   |
+| service             | v1.1.44        | 2026-01-13   |
+| AuthLayer           | v1.1.2         | 2026-01-13   |
+| UsersDB             | postgres:14.1  | 2026-01-13   |
+| TimDB               | postgres:14.1  | 2026-01-13   |
+| Backoffice DSL                 | backoffice-module-test-3.1.7-stage | 2026-01-13   |
+| Analytics DSL                 | analytics-module-test-1.6.14  | 2026-01-13   |
+| Training DSL                 | training-module-test-1.6.7  | 2026-01-13   |
+| Service DSL                 | service-module-test-1.6.3  | 2026-01-13   |
 ---
 
 ## Versioning Notes
```

## Change on 2026-02-25 15:58:10 (EET)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index b452918..f856ae2 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -14,7 +14,7 @@ Upcoming version - **V3.2.0**
 | Resql               | v1.3.5         | 2026-01-13   |
 | TIM                 | v2.3.6         | 2026-01-13   |
 | CronManager         | v1.1.41        | 2026-02-23   |
-| DataMapper          | v2.2.37        | 2026-02-23   |
+| DataMapper          | v2.2.38        | 2026-02-23   |
 | NotificationsNode   | v2.1.92-notification-node| 2026-02-23   |
 | OpenSearch          | 1.3.16         | 2026-01-13   |
 | S3Ferry             | pre-alpha-1.1.1| 2026-01-13   |
@@ -28,8 +28,8 @@ Upcoming version - **V3.2.0**
 | AuthLayer           | v1.1.2         | 2026-01-13   |
 | UsersDB             | postgres:14.1  | 2026-01-13   |
 | TimDB               | postgres:14.1  | 2026-01-13   |
-| Backoffice DSL                 | backoffice-module-test-3.2.18  | 2026-02-23   |
-| Analytics DSL                 | analytics-module-test-3.2.13  | 2026-02-23   |
+| Backoffice DSL                 | backoffice-module-test-3.2.21  | 2026-02-23   |
+| Analytics DSL                 | analytics-module-test-3.2.15  | 2026-02-23   |
 | Training DSL                 | training-module-test-3.2.9  | 2026-02-23   |
 | Service DSL                 | service-module-test-3.2.7  | 2026-02-23   |
 ---
```

## Change on 2026-03-02 13:23:10 (EET)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index f856ae2..1fbbc37 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -15,23 +15,23 @@ Upcoming version - **V3.2.0**
 | TIM                 | v2.3.6         | 2026-01-13   |
 | CronManager         | v1.1.41        | 2026-02-23   |
 | DataMapper          | v2.2.38        | 2026-02-23   |
-| NotificationsNode   | v2.1.92-notification-node| 2026-02-23   |
+| NotificationsNode   | v2.1.102-notification-node| 2026-03-02   |
 | OpenSearch          | 1.3.16         | 2026-01-13   |
 | S3Ferry             | pre-alpha-1.1.1| 2026-01-13   |
 | S3Ferry-publish     | pre-alpha-1.1.1| 2026-01-13   |
 | XTR                 | pre-alpha-test-1.1.3| 2026-01-13   |
 | widget              | v2.1.69        | 2026-02-23   |
-| backoffice          | v2.1.98        | 2026-02-23   |
-| analytics           | v1.1.48        | 2026-02-23   |
-| training            | v2.1.47        | 2026-02-23   |
-| service             | v1.1.53        | 2026-02-23   |
+| backoffice          | v2.1.102        | 2026-03-02   |
+| analytics           | v1.1.54        | 2026-03-02   |
+| training            | v2.1.48        | 2026-03-02   |
+| service             | v1.1.55        | 2026-03-02   |
 | AuthLayer           | v1.1.2         | 2026-01-13   |
 | UsersDB             | postgres:14.1  | 2026-01-13   |
 | TimDB               | postgres:14.1  | 2026-01-13   |
-| Backoffice DSL                 | backoffice-module-test-3.2.21  | 2026-02-23   |
-| Analytics DSL                 | analytics-module-test-3.2.15  | 2026-02-23   |
-| Training DSL                 | training-module-test-3.2.9  | 2026-02-23   |
-| Service DSL                 | service-module-test-3.2.7  | 2026-02-23   |
+| Backoffice DSL                 | backoffice-module-test-3.2.24  | 2026-03-02   |
+| Analytics DSL                 | analytics-module-test-3.2.16  | 2026-03-02   |
+| Training DSL                 | training-module-test-3.2.9  | 2026-03-02   |
+| Service DSL                 | service-module-test-3.2.8  | 2026-03-02   |
 ---
 
 
```

## Change on 2026-03-04 11:41:26 (EET)
**Author:** KlviG <78801020+KlviG@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index 1fbbc37..a1c7f27 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -22,14 +22,14 @@ Upcoming version - **V3.2.0**
 | XTR                 | pre-alpha-test-1.1.3| 2026-01-13   |
 | widget              | v2.1.69        | 2026-02-23   |
 | backoffice          | v2.1.102        | 2026-03-02   |
-| analytics           | v1.1.54        | 2026-03-02   |
+| analytics           | v1.1.55        | 2026-03-02   |
 | training            | v2.1.48        | 2026-03-02   |
 | service             | v1.1.55        | 2026-03-02   |
 | AuthLayer           | v1.1.2         | 2026-01-13   |
 | UsersDB             | postgres:14.1  | 2026-01-13   |
 | TimDB               | postgres:14.1  | 2026-01-13   |
 | Backoffice DSL                 | backoffice-module-test-3.2.24  | 2026-03-02   |
-| Analytics DSL                 | analytics-module-test-3.2.16  | 2026-03-02   |
+| Analytics DSL                 | analytics-module-test-3.2.19  | 2026-03-02   |
 | Training DSL                 | training-module-test-3.2.9  | 2026-03-02   |
 | Service DSL                 | service-module-test-3.2.8  | 2026-03-02   |
 ---
```

## Change on 2026-03-05 15:24:00 (EET)
**Author:** KlviG <78801020+KlviG@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index a1c7f27..4603297 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -13,7 +13,7 @@ Upcoming version - **V3.2.0**
 | Ruuter-Private      | v2.2.8         | 2026-01-13   |
 | Resql               | v1.3.5         | 2026-01-13   |
 | TIM                 | v2.3.6         | 2026-01-13   |
-| CronManager         | v1.1.41        | 2026-02-23   |
+| CronManager         | v1.1.42        | 2026-02-23   |
 | DataMapper          | v2.2.38        | 2026-02-23   |
 | NotificationsNode   | v2.1.102-notification-node| 2026-03-02   |
 | OpenSearch          | 1.3.16         | 2026-01-13   |
```

## Change on 2026-05-05 14:07:19 (EEST)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index 4603297..a027b90 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -17,7 +17,7 @@ Upcoming version - **V3.2.0**
 | DataMapper          | v2.2.38        | 2026-02-23   |
 | NotificationsNode   | v2.1.102-notification-node| 2026-03-02   |
 | OpenSearch          | 1.3.16         | 2026-01-13   |
-| S3Ferry             | pre-alpha-1.1.1| 2026-01-13   |
+| S3Ferry             | v1.1.2| 2026-01-13   |
 | S3Ferry-publish     | pre-alpha-1.1.1| 2026-01-13   |
 | XTR                 | pre-alpha-test-1.1.3| 2026-01-13   |
 | widget              | v2.1.69        | 2026-02-23   |
```

## Change on 2026-05-05 14:07:40 (EEST)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index a027b90..40ee73c 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -17,7 +17,7 @@ Upcoming version - **V3.2.0**
 | DataMapper          | v2.2.38        | 2026-02-23   |
 | NotificationsNode   | v2.1.102-notification-node| 2026-03-02   |
 | OpenSearch          | 1.3.16         | 2026-01-13   |
-| S3Ferry             | v1.1.2| 2026-01-13   |
+| S3Ferry             | v1.1.2         | 2026-05-05   |
 | S3Ferry-publish     | pre-alpha-1.1.1| 2026-01-13   |
 | XTR                 | pre-alpha-test-1.1.3| 2026-01-13   |
 | widget              | v2.1.69        | 2026-02-23   |
```

## Change on 2026-05-18 11:18:58 (EEST)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index 40ee73c..6f0955b 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -13,25 +13,25 @@ Upcoming version - **V3.2.0**
 | Ruuter-Private      | v2.2.8         | 2026-01-13   |
 | Resql               | v1.3.5         | 2026-01-13   |
 | TIM                 | v2.3.6         | 2026-01-13   |
-| CronManager         | v1.1.42        | 2026-02-23   |
-| DataMapper          | v2.2.38        | 2026-02-23   |
-| NotificationsNode   | v2.1.102-notification-node| 2026-03-02   |
+| CronManager         | v1.1.45        | 18-05-2026   |
+| DataMapper          | v2.2.42        | 18-05-2026   |
+| NotificationsNode   | v2.1.126-notification-node| 18-05-2026    |
 | OpenSearch          | 1.3.16         | 2026-01-13   |
-| S3Ferry             | v1.1.2         | 2026-05-05   |
+| S3Ferry             | v1.1.3         | 18-05-2026   |
 | S3Ferry-publish     | pre-alpha-1.1.1| 2026-01-13   |
 | XTR                 | pre-alpha-test-1.1.3| 2026-01-13   |
-| widget              | v2.1.69        | 2026-02-23   |
-| backoffice          | v2.1.102        | 2026-03-02   |
-| analytics           | v1.1.55        | 2026-03-02   |
-| training            | v2.1.48        | 2026-03-02   |
-| service             | v1.1.55        | 2026-03-02   |
+| widget              | v2.1.77        | 18-05-2026   |
+| backoffice          | v2.1.126        | 18-05-2026    |
+| analytics           | v1.1.67        | 18-05-2026   |
+| training            | v2.1.51        | 18-05-2026   |
+| service             | v1.1.65        | 18-05-2026   |
 | AuthLayer           | v1.1.2         | 2026-01-13   |
 | UsersDB             | postgres:14.1  | 2026-01-13   |
 | TimDB               | postgres:14.1  | 2026-01-13   |
-| Backoffice DSL                 | backoffice-module-test-3.2.24  | 2026-03-02   |
-| Analytics DSL                 | analytics-module-test-3.2.19  | 2026-03-02   |
-| Training DSL                 | training-module-test-3.2.9  | 2026-03-02   |
-| Service DSL                 | service-module-test-3.2.8  | 2026-03-02   |
+| Backoffice DSL                 | backoffice-module-test-3.2.1-stage  | 18-05-2026   |
+| Analytics DSL                 | analytics-module-test-3.2.1-stage  | 18-05-2026   |
+| Training DSL                 | training-module-test-3.2.1-stage  | 18-05-2026   |
+| Service DSL                 | service-module-test-3.2.1-stage  | 18-05-2026   |
 ---
 
 
```

## Change on 2026-05-25 10:10:29 (EEST)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index 6f0955b..4440b83 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -13,25 +13,25 @@ Upcoming version - **V3.2.0**
 | Ruuter-Private      | v2.2.8         | 2026-01-13   |
 | Resql               | v1.3.5         | 2026-01-13   |
 | TIM                 | v2.3.6         | 2026-01-13   |
-| CronManager         | v1.1.45        | 18-05-2026   |
+| CronManager         | v1.1.46        | 25-05-2026   |
 | DataMapper          | v2.2.42        | 18-05-2026   |
-| NotificationsNode   | v2.1.126-notification-node| 18-05-2026    |
+| NotificationsNode   | v2.1.130-notification-node| 25-05-2026    |
 | OpenSearch          | 1.3.16         | 2026-01-13   |
 | S3Ferry             | v1.1.3         | 18-05-2026   |
 | S3Ferry-publish     | pre-alpha-1.1.1| 2026-01-13   |
 | XTR                 | pre-alpha-test-1.1.3| 2026-01-13   |
 | widget              | v2.1.77        | 18-05-2026   |
-| backoffice          | v2.1.126        | 18-05-2026    |
-| analytics           | v1.1.67        | 18-05-2026   |
+| backoffice          | v2.1.130        | 25-05-2026    |
+| analytics           | v1.1.68        | 18-05-2026   |
 | training            | v2.1.51        | 18-05-2026   |
-| service             | v1.1.65        | 18-05-2026   |
+| service             | v1.1.68        | 18-05-2026   |
 | AuthLayer           | v1.1.2         | 2026-01-13   |
 | UsersDB             | postgres:14.1  | 2026-01-13   |
 | TimDB               | postgres:14.1  | 2026-01-13   |
-| Backoffice DSL                 | backoffice-module-test-3.2.1-stage  | 18-05-2026   |
-| Analytics DSL                 | analytics-module-test-3.2.1-stage  | 18-05-2026   |
-| Training DSL                 | training-module-test-3.2.1-stage  | 18-05-2026   |
-| Service DSL                 | service-module-test-3.2.1-stage  | 18-05-2026   |
+| Backoffice DSL                 | backoffice-module-test-3.2.3-stage  | 25-05-2026   |
+| Analytics DSL                 | analytics-module-test-3.2.3-stage  | 25-05-2026   |
+| Training DSL                 | training-module-test-3.2.3-stage  | 25-05-2026   |
+| Service DSL                 | service-module-test-3.2.3-stage  | 25-05-2026   |
 ---
 
 
```

## Change on 2026-05-25 10:27:01 (EEST)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index 4440b83..e95f379 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -24,7 +24,7 @@ Upcoming version - **V3.2.0**
 | backoffice          | v2.1.130        | 25-05-2026    |
 | analytics           | v1.1.68        | 18-05-2026   |
 | training            | v2.1.51        | 18-05-2026   |
-| service             | v1.1.68        | 18-05-2026   |
+| service             | v1.1.69        | 25-05-2026   |
 | AuthLayer           | v1.1.2         | 2026-01-13   |
 | UsersDB             | postgres:14.1  | 2026-01-13   |
 | TimDB               | postgres:14.1  | 2026-01-13   |
```

## Change on 2026-05-25 12:35:29 (EEST)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index e95f379..3d9677a 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -28,7 +28,7 @@ Upcoming version - **V3.2.0**
 | AuthLayer           | v1.1.2         | 2026-01-13   |
 | UsersDB             | postgres:14.1  | 2026-01-13   |
 | TimDB               | postgres:14.1  | 2026-01-13   |
-| Backoffice DSL                 | backoffice-module-test-3.2.3-stage  | 25-05-2026   |
+| Backoffice DSL                 | backoffice-module-test-3.2.4-stage  | 25-05-2026   |
 | Analytics DSL                 | analytics-module-test-3.2.3-stage  | 25-05-2026   |
 | Training DSL                 | training-module-test-3.2.3-stage  | 25-05-2026   |
 | Service DSL                 | service-module-test-3.2.3-stage  | 25-05-2026   |
```

## Change on 2026-05-26 12:27:14 (EEST)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index 3d9677a..ebea9ea 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -15,23 +15,23 @@ Upcoming version - **V3.2.0**
 | TIM                 | v2.3.6         | 2026-01-13   |
 | CronManager         | v1.1.46        | 25-05-2026   |
 | DataMapper          | v2.2.42        | 18-05-2026   |
-| NotificationsNode   | v2.1.130-notification-node| 25-05-2026    |
+| NotificationsNode   | v2.1.134-notification-node| 26-05-2026    |
 | OpenSearch          | 1.3.16         | 2026-01-13   |
 | S3Ferry             | v1.1.3         | 18-05-2026   |
 | S3Ferry-publish     | pre-alpha-1.1.1| 2026-01-13   |
 | XTR                 | pre-alpha-test-1.1.3| 2026-01-13   |
-| widget              | v2.1.77        | 18-05-2026   |
-| backoffice          | v2.1.130        | 25-05-2026    |
-| analytics           | v1.1.68        | 18-05-2026   |
+| widget              | v2.1.78        | 26-05-2026   |
+| backoffice          | v2.1.134        | 26-05-2026    |
+| analytics           | v1.1.69        | 26-05-2026   |
 | training            | v2.1.51        | 18-05-2026   |
 | service             | v1.1.69        | 25-05-2026   |
 | AuthLayer           | v1.1.2         | 2026-01-13   |
 | UsersDB             | postgres:14.1  | 2026-01-13   |
 | TimDB               | postgres:14.1  | 2026-01-13   |
-| Backoffice DSL                 | backoffice-module-test-3.2.4-stage  | 25-05-2026   |
-| Analytics DSL                 | analytics-module-test-3.2.3-stage  | 25-05-2026   |
-| Training DSL                 | training-module-test-3.2.3-stage  | 25-05-2026   |
-| Service DSL                 | service-module-test-3.2.3-stage  | 25-05-2026   |
+| Backoffice DSL                 | backoffice-module-test-3.2.5-stage  | 26-05-2026   |
+| Analytics DSL                 | analytics-module-test-3.2.5-stage  | 26-05-2026   |
+| Training DSL                 | training-module-test-3.2.5-stage  | 26-05-2026   |
+| Service DSL                 | service-module-test-3.2.5-stage  | 26-05-2026   |
 ---
 
 
```

## Change on 2026-05-27 12:01:40 (EEST)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index ebea9ea..4b83b3f 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -15,23 +15,23 @@ Upcoming version - **V3.2.0**
 | TIM                 | v2.3.6         | 2026-01-13   |
 | CronManager         | v1.1.46        | 25-05-2026   |
 | DataMapper          | v2.2.42        | 18-05-2026   |
-| NotificationsNode   | v2.1.134-notification-node| 26-05-2026    |
+| NotificationsNode   | v2.1.135-notification-node| 26-05-2026    |
 | OpenSearch          | 1.3.16         | 2026-01-13   |
 | S3Ferry             | v1.1.3         | 18-05-2026   |
 | S3Ferry-publish     | pre-alpha-1.1.1| 2026-01-13   |
 | XTR                 | pre-alpha-test-1.1.3| 2026-01-13   |
 | widget              | v2.1.78        | 26-05-2026   |
-| backoffice          | v2.1.134        | 26-05-2026    |
+| backoffice          | v2.1.135        | 27-05-2026    |
 | analytics           | v1.1.69        | 26-05-2026   |
 | training            | v2.1.51        | 18-05-2026   |
 | service             | v1.1.69        | 25-05-2026   |
 | AuthLayer           | v1.1.2         | 2026-01-13   |
 | UsersDB             | postgres:14.1  | 2026-01-13   |
 | TimDB               | postgres:14.1  | 2026-01-13   |
-| Backoffice DSL                 | backoffice-module-test-3.2.5-stage  | 26-05-2026   |
-| Analytics DSL                 | analytics-module-test-3.2.5-stage  | 26-05-2026   |
-| Training DSL                 | training-module-test-3.2.5-stage  | 26-05-2026   |
-| Service DSL                 | service-module-test-3.2.5-stage  | 26-05-2026   |
+| Backoffice DSL                 | backoffice-module-test-3.2.6-stage  | 27-05-2026   |
+| Analytics DSL                 | analytics-module-test-3.2.6-stage  | 27-05-2026   |
+| Training DSL                 | training-module-test-3.2.6-stage  | 27-05-2026   |
+| Service DSL                 | service-module-test-3.2.6-stage  | 27-05-2026   |
 ---
 
 
```

## Change on 2026-06-01 14:11:39 (EEST)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index 4b83b3f..5faeac1 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -13,22 +13,22 @@ Upcoming version - **V3.2.0**
 | Ruuter-Private      | v2.2.8         | 2026-01-13   |
 | Resql               | v1.3.5         | 2026-01-13   |
 | TIM                 | v2.3.6         | 2026-01-13   |
-| CronManager         | v1.1.46        | 25-05-2026   |
+| CronManager         | v1.1.47        | 01-06-2026   |
 | DataMapper          | v2.2.42        | 18-05-2026   |
-| NotificationsNode   | v2.1.135-notification-node| 26-05-2026    |
+| NotificationsNode   | v2.1.136-notification-node| 01-06-2026    |
 | OpenSearch          | 1.3.16         | 2026-01-13   |
 | S3Ferry             | v1.1.3         | 18-05-2026   |
 | S3Ferry-publish     | pre-alpha-1.1.1| 2026-01-13   |
 | XTR                 | pre-alpha-test-1.1.3| 2026-01-13   |
-| widget              | v2.1.78        | 26-05-2026   |
-| backoffice          | v2.1.135        | 27-05-2026    |
-| analytics           | v1.1.69        | 26-05-2026   |
+| widget              | v2.1.79        | 01-06-2026   |
+| backoffice          | v2.1.136        | 01-06-2026    |
+| analytics           | v1.1.70        | 01-06-2026   |
 | training            | v2.1.51        | 18-05-2026   |
-| service             | v1.1.69        | 25-05-2026   |
+| service             | v1.1.70        | 01-06-2026   |
 | AuthLayer           | v1.1.2         | 2026-01-13   |
 | UsersDB             | postgres:14.1  | 2026-01-13   |
 | TimDB               | postgres:14.1  | 2026-01-13   |
-| Backoffice DSL                 | backoffice-module-test-3.2.6-stage  | 27-05-2026   |
+| Backoffice DSL                 | backoffice-module-test-3.2.85-jira  | 01-06-2026   |
 | Analytics DSL                 | analytics-module-test-3.2.6-stage  | 27-05-2026   |
 | Training DSL                 | training-module-test-3.2.6-stage  | 27-05-2026   |
 | Service DSL                 | service-module-test-3.2.6-stage  | 27-05-2026   |
```

## Change on 2026-06-02 10:57:53 (EEST)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index 0755065..1143ff8 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -28,7 +28,7 @@ Upcoming version - **V3.3.0**
 | AuthLayer           | v1.1.2         | 2026-01-13   |
 | UsersDB             | postgres:14.1  | 2026-01-13   |
 | TimDB               | postgres:14.1  | 2026-01-13   |
-| Backoffice DSL                 | backoffice-module-test-3.2.85-jira  | 01-06-2026   |
+| Backoffice DSL                 | backoffice-module-test-3.3.0 | 02-06-2026   |
 | Analytics DSL                 | analytics-module-test-3.2.6-stage  | 27-05-2026   |
 | Training DSL                 | training-module-test-3.2.6-stage  | 27-05-2026   |
 | Service DSL                 | service-module-test-3.2.6-stage  | 27-05-2026   |
```

## Change on 2026-06-16 11:17:48 (EEST)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index 1143ff8..ccb9809 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -13,25 +13,25 @@ Upcoming version - **V3.3.0**
 | Ruuter-Private      | v2.2.8         | 2026-01-13   |
 | Resql               | v1.3.5         | 2026-01-13   |
 | TIM                 | v2.3.6         | 2026-01-13   |
-| CronManager         | v1.1.47        | 01-06-2026   |
-| DataMapper          | v2.2.42        | 18-05-2026   |
-| NotificationsNode   | v2.1.136-notification-node| 01-06-2026    |
+| CronManager         | v1.1.51        | 16-06-2026   |
+| DataMapper          | v2.2.43        | 16-06-2026   |
+| NotificationsNode   | v2.1.147-notification-node| 01-06-2026    |
 | OpenSearch          | 1.3.16         | 2026-01-13   |
 | S3Ferry             | v1.1.3         | 18-05-2026   |
 | S3Ferry-publish     | pre-alpha-1.1.1| 2026-01-13   |
 | XTR                 | pre-alpha-test-1.1.3| 2026-01-13   |
-| widget              | v2.1.79        | 01-06-2026   |
-| backoffice          | v2.1.136        | 01-06-2026    |
-| analytics           | v1.1.70        | 01-06-2026   |
+| widget              | v2.1.80        | 16-06-2026   |
+| backoffice          | v2.1.147        | 16-06-2026    |
+| analytics           | v1.1.79        | 16-06-2026   |
 | training            | v2.1.51        | 18-05-2026   |
-| service             | v1.1.70        | 01-06-2026   |
+| service             | v1.1.75        | 16-06-2026   |
 | AuthLayer           | v1.1.2         | 2026-01-13   |
 | UsersDB             | postgres:14.1  | 2026-01-13   |
 | TimDB               | postgres:14.1  | 2026-01-13   |
-| Backoffice DSL                 | backoffice-module-test-3.3.0 | 02-06-2026   |
-| Analytics DSL                 | analytics-module-test-3.2.6-stage  | 27-05-2026   |
-| Training DSL                 | training-module-test-3.2.6-stage  | 27-05-2026   |
-| Service DSL                 | service-module-test-3.2.6-stage  | 27-05-2026   |
+| Backoffice DSL                 | backoffice-module-test-3.3.1-stage | 16-06-2026   |
+| Analytics DSL                 | analytics-module-test-3.3.1-stage  | 16-06-2026   |
+| Training DSL                 | training-module-test-3.3.1-stage  | 16-06-2026   |
+| Service DSL                 | service-module-test-3.3.1-stage  | 16-06-2026   |
 ---
 
 
```

## Change on 2026-06-17 13:46:34 (EEST)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index ccb9809..8db6f8e 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -29,7 +29,7 @@ Upcoming version - **V3.3.0**
 | UsersDB             | postgres:14.1  | 2026-01-13   |
 | TimDB               | postgres:14.1  | 2026-01-13   |
 | Backoffice DSL                 | backoffice-module-test-3.3.1-stage | 16-06-2026   |
-| Analytics DSL                 | analytics-module-test-3.3.1-stage  | 16-06-2026   |
+| Analytics DSL                 | analytics-module-test-3.3.2-stage  | 17-06-2026   |
 | Training DSL                 | training-module-test-3.3.1-stage  | 16-06-2026   |
 | Service DSL                 | service-module-test-3.3.1-stage  | 16-06-2026   |
 ---
```

## Change on 2026-07-06 10:18:48 (EEST)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index 8db6f8e..8654b0e 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -14,24 +14,24 @@ Upcoming version - **V3.3.0**
 | Resql               | v1.3.5         | 2026-01-13   |
 | TIM                 | v2.3.6         | 2026-01-13   |
 | CronManager         | v1.1.51        | 16-06-2026   |
-| DataMapper          | v2.2.43        | 16-06-2026   |
-| NotificationsNode   | v2.1.147-notification-node| 01-06-2026    |
+| DataMapper          | v2.2.44        | 03-07-2026   |
+| NotificationsNode   | v2.1.149-notification-node| 03-07-2026    |
 | OpenSearch          | 1.3.16         | 2026-01-13   |
 | S3Ferry             | v1.1.3         | 18-05-2026   |
 | S3Ferry-publish     | pre-alpha-1.1.1| 2026-01-13   |
 | XTR                 | pre-alpha-test-1.1.3| 2026-01-13   |
 | widget              | v2.1.80        | 16-06-2026   |
-| backoffice          | v2.1.147        | 16-06-2026    |
-| analytics           | v1.1.79        | 16-06-2026   |
+| backoffice          | v2.1.149        | 03-07-2026    |
+| analytics           | v1.1.82        | 03-07-2026   |
 | training            | v2.1.51        | 18-05-2026   |
-| service             | v1.1.75        | 16-06-2026   |
+| service             | v1.1.76        | 03-07-2026   |
 | AuthLayer           | v1.1.2         | 2026-01-13   |
 | UsersDB             | postgres:14.1  | 2026-01-13   |
 | TimDB               | postgres:14.1  | 2026-01-13   |
-| Backoffice DSL                 | backoffice-module-test-3.3.1-stage | 16-06-2026   |
-| Analytics DSL                 | analytics-module-test-3.3.2-stage  | 17-06-2026   |
-| Training DSL                 | training-module-test-3.3.1-stage  | 16-06-2026   |
-| Service DSL                 | service-module-test-3.3.1-stage  | 16-06-2026   |
+| Backoffice DSL                 | backoffice-module-test-3.3.12 | 03-07-2026   |
+| Analytics DSL                 | analytics-module-test-3.3.14  | 03-07-2026   |
+| Training DSL                 | training-module-test-3.3.5  | 03-07-2026   |
+| Service DSL                 | service-module-test-3.3.7  | 03-07-2026   |
 ---
 
 
```

## Change on 2026-07-07 14:06:08 (EEST)
**Author:** ffrose <119657383+ffrose@users.noreply.github.com>

```diff
diff --git a/VERSIONS.md b/VERSIONS.md
index 8654b0e..7854bb6 100644
--- a/VERSIONS.md
+++ b/VERSIONS.md
@@ -4,7 +4,7 @@ All application version numbers listed here represent the latest available **rel
 
 
 
-Upcoming version - **V3.3.0**
+Upcoming version - **V3.3.1**
 ---
 
 | Application         | Latest Version | Release Date |
```

