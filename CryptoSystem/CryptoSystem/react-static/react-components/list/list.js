const List = props => {
  const [position, setPosition] = React.useState(0);
  const [dragStart, setDragStart] = React.useState(0);
  const [dragPositionStart, setDragPositionStart] = React.useState(0);
  const [isBeingDragged, setIsBeingDragged] = React.useState(false);
  const listItems = React.useRef(null);
  const list = React.useRef(null);
  const [style, setStyle] = React.useState({});
  const children = {};

  const moveList = newPos => {
    // translate the list to newPos
    setStyle({
      transform: `translate(${position}px,0)`
    });

    if (newPos < -getEndOfList() && newPos < position) {
      // console.log("newPos", newPos)
      // console.log("getEndoflist", getEndOfList())
      return;
    } else if (newPos > 0) {
      setPosition(0);
    } else if (position !== newPos) {
      setPosition(newPos);
    }
  };

  const whenDragStart = clientX => {
    setDragStart(clientX);
    setIsBeingDragged(true);
    setDragPositionStart(position);
  };

  const whenDrag = clientX => {
    let diff = clientX - dragStart;
    let newPos = dragPositionStart + diff;
    moveList(newPos);
  };

  const whenDragStop = () => {
    setIsBeingDragged(false);
    moveToGrid(position);
  };

  const handleMouseMove = e => {
    e.preventDefault();

    if (e.buttons === 1) {
      if (isBeingDragged === false) {
        whenDragStart(e.clientX);
      } else {
        whenDrag(e.clientX);
      }
    } else if (e.buttons === 0 && isBeingDragged === true) {
      whenDragStop();
    }
  };

  const getEndOfList = () => {
    let listWidth = list.current.offsetWidth;
    let listItemsWidth = listItems.current.scrollWidth;
    console.log("listWidth", listWidth);
    console.log("listItemsWidth", listItemsWidth);
    return listItemsWidth - listWidth;
  };

  const moveToGrid = start => {
    let gridsize = children[0].current.offsetWidth + props.columnGapPx;
    let nearestMultiple = gridsize * Math.ceil((-start - gridsize / 2) / gridsize);
    let endOfList = getEndOfList();
    let finalDestination = Math.abs(-position - nearestMultiple) < Math.abs(-position - endOfList) ? nearestMultiple : endOfList + 12;
    setPosition(-finalDestination);
    setStyle({
      transform: `translate(${-finalDestination}px, 0)`,
      transition: `transform .4s ease-out`
    });
  };

  const getRefsFromListItems = (listItemRef, key) => {
    children[key] = listItemRef;
  };

  const childrenWithExtraProps = () => {
    // add extra props to the children
    return React.Children.map(props.children, child => {
      return React.cloneElement(child, {
        unSelectedSize: props.unSelectedSize,
        selectedSize: props.selectedSize,
        passRefUpward: getRefsFromListItems
      });
    });
  };

  return /*#__PURE__*/React.createElement("div", {
    className: "list",
    ref: list
  }, /*#__PURE__*/React.createElement("span", {
    className: "title"
  }, props.title), /*#__PURE__*/React.createElement("div", {
    className: "listitems",
    ref: listItems,
    onMouseMove: handleMouseMove,
    style: style
  }, childrenWithExtraProps()));
};

export default List;