#!/bin/bash
# Open all deployed dashboards in the default browser. Replace YOUR_NETLIFY_SITE_NAME with your actual Netlify site name.

SITE="YOUR_NETLIFY_SITE_NAME"

open -a "Google Chrome" "https://3dmark-pro--$SITE.netlify.app/"
open -a "Google Chrome" "https://$SITE.netlify.app/3dmark-pro.html"
open -a "Google Chrome" "https://gis--$SITE.netlify.app/"
open -a "Google Chrome" "https://$SITE.netlify.app/gis.html"
open -a "Google Chrome" "https://gen3d--$SITE.netlify.app/"
open -a "Google Chrome" "https://$SITE.netlify.app/gen3d.html"
