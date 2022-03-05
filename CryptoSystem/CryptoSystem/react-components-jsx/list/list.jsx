const List = (props) => {
    
    const [position, setPosition] = React.useState(0);
    const [dragStart, setDragStart] = React.useState(0);
    const [dragPositionStart, setDragPositionStart] = React.useState(0);
    const [isBeingDragged, setIsBeingDragged] = React.useState(false);
    const listItems=React.useRef(null);
    const list=React.useRef(null)
    const [style, setStyle] = React.useState({})


    const moveList = (newPos) => {
        // translate the list to newPos
        setStyle({transform:`translate(${position}px,0)`})

        let listItemsRight = listItems.current ? listItems.current.getBoundingClientRect().right : 0;
        let listRight = listItems.current ? list.current.getBoundingClientRect().right : 0;

        if ( (listItemsRight <= listRight) && (newPos < position)) {
            return
        } else if(newPos > 0){
            setPosition(0)
        } else if ( position !== newPos) {
            setPosition(newPos);
        }
    }

    const whenDragStart = (clientX) => {
        setDragStart(clientX);
        setIsBeingDragged(true);
        setDragPositionStart(position)        
    }

    const whenDrag = (clientX) => {
        let diff = clientX - dragStart;
        let newPos = dragPositionStart + diff;
        moveList(newPos);        
    }

    const whenDragStop = () => {
        setIsBeingDragged(false);
        moveToGrid(position)        
    }

    const handleMouseMove = (e) => {
        e.preventDefault()
        if(e.buttons === 1){
            if(isBeingDragged === false){
                whenDragStart(e.clientX)
            } else {
                whenDrag(e.clientX)
            }
        } else if ((e.buttons === 0) && (isBeingDragged === true)) {
            whenDragStop()
        }
    }

    const moveToGrid = (start) => {
        let gridsize = props.unSelectedSize + props.columnGapPx
        let nearestMultiple = gridsize*(Math.ceil((-start - gridsize/2) / gridsize))

        setPosition(-nearestMultiple)
        setStyle({transform:`translate(${-nearestMultiple}px, 0)`,
            transition:`transform .4s ease-out`})

    }


    const childrenWithWidth = () => {
        // add extra props to the children
        return React.Children.map(props.children, child => {
            return React.cloneElement(child,{
                unSelectedSize:props.unSelectedSize,
                selectedSize:props.selectedSize,
            });
        });
        
    }

    return (
        <div className="list"
            ref={list}>
            <span>{position}</span>

            <div className="listitems" 
                ref={listItems} 
                onMouseMove={handleMouseMove}
                style={style}
            >
                {childrenWithWidth()}
            </div>                

        </div>
    )
}

export default List