import List from "../list/list.js"
import ListItem from "../listItem/listItem.js"

const Portfolio = () => {
    
    const [topList, setTopList] = React.useState();
    const [hotList, setHotList] = React.useState();
        
    const createList = (title, api_response) => {
        return <List title={title}
        unSelectedSize={240}
        selectedSize={300}
        columnGapPx={24}
        key={title}>
                {getNFTs(api_response)}
        </List>
    }
    const getNFTs = (api_response) => {
        return api_response.list.map( function (collection) {
            if(collection.pic == null){
                return
            }
            return <ListItem
                url = {"https://rarible.com/"+collection.shortUrl}
                img = {collection.pic}
                collection_name = {collection.name}
                price = {collection.sum}
                count = {collection.count}
                currency = {collection.currency}
                id = {collection.id}
                key = {collection.id}
                />
        })
    }
    
    const getResponse = (url, handler) => {
        fetch(url, {
            "method": "GET",     
        })
        // read the data in json file
        .then(response => response.json())
        .then(response => {
            handler(response)
        })
        .catch(err => {
            console.error(err);
        });        
    }

    React.useEffect( function() {
        var url = window.location.href;
        var arr = url.split("/");
        var result = arr[0] + "//" + arr[2];        
        getResponse(result+"/nft-api/top", (response) => setTopList(createList("Top Collections", response)))
        getResponse(result+"/nft-api/hot", (response) => setHotList(createList("Trending Collections", response)))
    }, [])
    
    return (        
        <section className="portfolio">
            {topList}
            {hotList}
        </section>
    )
}
ReactDOM.render(React.createElement(Portfolio), document.querySelector("#pricetable"))