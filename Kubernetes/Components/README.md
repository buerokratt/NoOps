##### Changes that are needed

    - configmap:
        Change, delete or add constants.ini content according to needs
    - ingress:
        depending on networking, change `path: "/` to reflect necessary subpath's. Example: `path: "/v2/public/(.*)"`
        Change the parameters for cors.
