##### Changes that are needed

Helm changes  
    - configmap:
        Change, delete or add constants.ini content according to needs
    - ingress:
        depending on networking, change `path: "/` to reflect necessary subpath's. Example: `path: "/v2/public/(.*)"`
        Change the parameters for cors.

Module changes (if necessary)
    - TIM: jwt_allowlit needs a ubnet to be added, for pods to communicate correctly, otherwise might face the tara auth issues