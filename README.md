# Animal Adoption Web Application

This is a group Capstone Web App Project built for CS467 W2021. 

## Project Idea:

  * Social Playlist Site
  * Where users can share playlists.
  * Create, upload playlists.
  * Link to 3rd party sources: Youtube, Twitter.
  * URL shortener.

## Motivation

  * This project has low criticality, as there is no high risk use that requires a feature set be perfect and/or thoroughly tested before deployment -- no one is at risk if a playlist is malformed. 
  
  * Moreover, because this a consumer application it would greatly benefit from the organic evolution of features the agile method facilitates. 
  
  * Incremental feature growth and iterative product cycles both add to the strengths of the agile method here; constant customer feedback will ensure the right product with the highest usability get built.

## Contributors:

  * Gregory Bauer
  * Amy Robertson
  * Jasper Wong  

## Quickstart

examples users

admin@example.com : admin
guest@example.com : guest


```
flask shell
>>> from socialPlaylist import db
>>> db.create_all()
