const ListItem = (props) => {
    const listItem=React.useRef()

    React.useEffect(function(){
        props.passRefUpward(listItem, props.id)
    })

    return (
        <div className="listitem"
            ref={listItem}
            // style={{
            //     width:`${props.unSelectedSize}px`, 
            //     height:`${props.unSelectedSize}px`
            //     }}
            styel={{
                width:"fit-content"
            }}
        >

            <img className="image" 
                src={props.img} 
                alt={`nft for ${props.nft_name}`}
                onDragStart={(e) => e.preventDefault()}
            /> 

            <span className="nft_name">{props.nft_name}</span>
            <span className="owner">{props.owner}</span>
            <div className="buy">
                <a className="button" href="buy">Buy </a>                
                <span className="price">{props.price}</span>
            </div>

        </div>
    )
}

export default ListItem