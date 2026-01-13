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

