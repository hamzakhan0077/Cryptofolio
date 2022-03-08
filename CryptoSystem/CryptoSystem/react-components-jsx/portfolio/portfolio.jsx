import List from "../list/list.js"
import ListItem from "../listItem/listItem.js"

const Portfolio = () => {
    // const list = <List>title={"title"} 
    //     unSelectedSize={240} 
    //     selectedSize={300} 
    //     columnGapPx={24}
    //     <ListItem 
    //                 img={"https://picsum.photos/200/200"} 
    //                 nft_name={""}
    //                 owner={"owner"}
    //             />
    //             <ListItem 
    //                 img={"https://picsum.photos/200/200"} 
    //                 nft_name={"nft name"}
    //                 owner={"owner"}
    //             />
    // </List>
    let collectionLists = [
        {
            key:0,
            items:[
                {
                    key:0,
                    name:'Collection name',
                    imageUrl:'https://picsum.photos/200/200',
                    price:32,
                    currency:"ETH",
                    count:300,
                },
            ],
        },
    ]

    const getNFTs = (collectionList) => {
        return collectionList.items.map( function (collection) {
            return <ListItem
                img = {collection.imageUrl}
                collection_name = {collection.name}
                price = {collection.price}
                count = {collection.count}
                currency = {collection.currency}
                id = {collection.key}
                key = {collection.key}
                />
        })
    }

    const list = collectionLists.map(function (collectionList) {
        return <List title={collectionList.name}
            unSelectedSize={240}
            selectedSize={300}
            columnGapPx={24}
            key={collectionList.key}>
                {getNFTs(collectionList)}
        </List>
    })

    return (        
        <section className="portfolio">
            {list}
        </section>
    )
}
ReactDOM.render(React.createElement(Portfolio), document.querySelector("#pricetable"))