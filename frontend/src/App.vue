<template>
  <div id="app">
    <label for="size">Choose Board size</label>
    <input id="size" v-model="sizeInput" v-on:input="sizeChanged" />
    <button v-on:click="small">Easy</button>
    <button v-on:click="medium">Normal</button>
    <button v-on:click="big">Hard</button>

    <div
      v-if="boardReady"
      id="board"
      :style="{
        gridTemplateColumns: getGridRowColumnsSize(),
        gridTemplateRows: getGridRowColumnsSize(),
      }"
    >
      <div
        class="card"
        v-on:click="getCard($event, k)"
        v-for="k in size * size"
        :key="k"
        :style="{ backgroundColor: getBackgroundColorOfCard(k) }"
      >
        <img v-if="getCardValue(k) != '' && getCardValue(k) <= 50" style="width: 80%; height: 80%" :src="'images/'+getCardValue(k)+'.png'"/>
        <p v-if="getCardValue(k) > 50">{{getCardValue(k)}}</p>
      </div>
    </div>
    <p v-if="boardKeys.length == 0 && boardReady">Congrats</p>
  </div>
</template>

<script>
import axios from "axios";

let server = "http://localhost:3000";

export default {
  name: "App",
  components: {},
  mounted() {
    this.initBoard();
  },
  data: function () {
    return {
      sizeInput: "1",
      size: 2,
      boardReady: false,
      selected: [],
      boardKeys: [],
      cardValues: {},
    };
  },
  computed: {
    
  },
  methods: {
    getBackgroundColorOfCard(k) {
      if (!this.boardKeys.includes(k)) return "gray";
      else return "bisque";
    },
    getCardValue(k) {
      if (this.cardValues[k]) return this.cardValues[k];
      else return "";
    },
    getCard(event, k) {
      if (this.selected.length >= 2) return;
      if (this.selected.includes(k)) return;
      if (!this.boardKeys.includes(k)) return;
      axios
        .post(server + "/get-card", {
          index: k,
        })
        .then((d) => {
          if (d.status != 200) {
            alert(d.data.msg);
          } else {
            this.cardValues[k] = d.data.msg;
            this.selected.push(k);
            if (this.selected.length == 2) {
              setTimeout(() => {
                this.submit();
              }, 500);
            }
            this.getBoard();
          }
        })
        .catch((err) => {
          alert(err.toString());
        });
    },
    initBoard() {
      // send request to flask and get redis ready
      axios
        .post(server + "/init", {
          size: this.size,
        })
        .then((d) => {
          if (d.status != 200) {
            alert(d.data.msg);
          } else {
            this.boardReady = true;
            this.getBoard();
          }
        })
        .catch((err) => {
          alert(err.toString());
        });
        this.selected = []
        this.cardValues = {}
    },
    getBoard() {
      axios
        .get(server + "/get-board")
        .then((d) => {
          if (d.status != 200) {
            alert("Could not reach to server");
          } else {
            this.boardKeys = d.data.keys;
          }
        })
        .catch((err) => {
          alert(err.toString());
        });
    },
    getGridRowColumnsSize() {
      let css = "auto";
      for (let i = 0; i < this.size - 1; i++) {
        css += " auto";
      }
      return css;
    },
    setBoardSize(size) {
      this.size = size*2;
      this.sizeInput = size.toString();
      this.boardReady = false;
      this.initBoard();
    },
    small() {
      this.setBoardSize(1);
    },
    medium() {
      this.setBoardSize(2);
    },
    big() {
      this.setBoardSize(4);
    },
    sizeChanged() {
      if (this.sizeInput === "") {
        this.size = 2;
        this.boardReady = false;
        this.initBoard();
      } else {
        try {
          if (parseInt(this.sizeInput) > 5) {
            alert("Size cannot be more than 5");
            this.setBoardSize(10);
            return;
          }
          this.setBoardSize(parseInt(this.sizeInput));
        } catch (error) {
          this.setBoardSize(2);
        }
      }
    },
    submit() {
      if (this.selected.length != 2) return;
      axios
        .post(server + "/submit", {
          index1: this.selected[0],
          index2: this.selected[1],
        })
        .then(() => {

        })
        .catch((err) => {
         
          if (err.response) {
            console.log("");
          } else if (err.request) {
            alert("No response from server");
          } else {
            alert("Error " + err.toString());
          }
        })
        this.cardValues = {};
        this.selected = [];
        setTimeout(() => { // give time to flask and redis to delete keys
          this.getBoard();
        }, 300)

    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
#board {
  margin-top: 1rem;
  display: grid;
  gap: 10px;
  justify-content: center;
  align-items: center;
}
.card {
  width: 4rem;
  height: 4rem;
  border: 1px solid black;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
}
.card:hover {
  background-color: cornflowerblue !important;
}
</style>
