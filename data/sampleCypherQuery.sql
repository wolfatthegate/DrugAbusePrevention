CALL apoc.load.json("file:////Users/julinamaharjan/Desktop/drugAbuse/tweets.json") YIELD value
unwind [value] as v
with v,  v.user as u, v.place as pp, v.entities as e
unwind pp.bounding_box.coordinates as bb


//merge (p:place { id:pp.id, bounding_box : bb, place_type:pp.place_type, name:pp.name, country_code: pp.country_code, url: '', country: pp.country, full_name:pp.full_name})
merge (p:place { id:pp.id, place_type:pp.place_type, name:pp.name, country_code: pp.country_code, url: '', country: pp.country, full_name:pp.full_name})
merge (me:user {id:u.id} ) on create set me+=u
merge (l:place {full_name:u.location})

MERGE (me)-[:at]->(l)
//SET t.text = v.text, t.created_at = v.created_at, t.retweet_count = v.retweet_count, t.favorite_count = v.favorite_count

merge (t:tweet {id:v.id_str}) on create set t+=v
//FOREACH (key IN keys(v) | SET t.key = v.key)
MERGE (me)-[:send]->(t)
MERGE (t)-[:tag]->(p)

FOREACH (f IN e.hashtags | 
    merge (h:hashtag {id: f.text}) on create set h+=f
    MERGE (t)-[:tag]->(h))
FOREACH (f IN e.urls | 
    merge (url:url {id: f.url}) on create set url+=f
    MERGE (t)-[:include]->(url))
FOREACH (f IN e.media | 
    merge (m:media {id: f.id}) on create set  m+=f
    MERGE (t)-[:has]->(url))
FOREACH (f IN e.user_mentions | 
    merge (u1:user {id:f.id})
    MERGE (t)-[:mention]->(u1))