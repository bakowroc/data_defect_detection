import * as React from "react";

export const style: {[key: string]: React.CSSProperties} = {
  selectors: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    padding: 15,
    height: '40px',
    width: '100vw',
    zIndex: 10,
    display: 'flex',
    flexDirection: 'row',
    background: '#006ec7'
  },
  definition: {
    color: 'white',
    fontSize: 11,
    display: 'flex',
    flexDirection: 'column',
    marginLeft: 'auto',
    paddingRight: 40
  },
  p: {
    margin: '1px'
  },
  button: {
    marginLeft: 50
  },
  loading: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    position: 'fixed',
    top: 0,
    bottom: 0,
    right: 0,
    left: 0,
    zIndex: 1000,
    background: 'rgba(0,0,0,0.3)'
  },
  spinner: {
    background: 'white',
    padding: 50
  }
};