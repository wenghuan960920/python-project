// 输入添加到列表里功能:
<my-component
  v-for="(item, index) in items"
  v-bind:item="item"
  v-bind:index="index"
  v-bind:key="item.id"
></my-component>

<div id="todo-list-example">
  <form v-on:submit.prevent="addNewTodo">
    <label for="new-todo">Add a todo</label>
    <input
      v-model="newTodoText"
      id="new-todo"
      placeholder="E.g. Feed the cat"
    >
    <button>Add</button>
  </form>

  <ul>
    <li
      is="todo-item"
      v-for="(todo, index) in todos"
      v-bind:key="todo.id"
      v-bind:title="todo.title"
      v-on:remove="todos.splice(index, 1)"
    ></li>
  </ul>
</div>


Vue.component('todo-item', {
  template: '\
    <li>\
      {{ title }}\
      <button v-on:click="$emit(\'remove\')">Remove</button>\
    </li>\
  ',
  props: ['title']
})

new Vue({
  el: '#todo-list-example',
  data: {
    newTodoText: '',
    todos: [
      {
        id: 1,
        title: 'Do the dishes',
      },
      {
        id: 2,
        title: 'Take out the trash',
      },
      {
        id: 3,
        title: 'Mow the lawn'
      }
    ],
    nextTodoId: 4
  },
  methods: {
    addNewTodo: function () {
      this.todos.push({
        id: this.nextTodoId++,
        title: this.newTodoText
      })
      this.newTodoText = ''
    }
  }
})

#使用复选框的方式去给列表中添加路径值得方法。
 https://cn.vuejs.org/v2/guide/forms.html#%E5%A4%8D%E9%80%89%E6%A1%86


<script>
      export default {

        data() {
          return {
            props: {
              label: 'name',
              children: 'zones'
            },
            count: 1
          };
        },

        methods: {
          handleCheckChange(data, checked, indeterminate) {
            console.log(data, checked, indeterminate);
          },
          handleNodeClick(data) {
            console.log(data);
          },
            // 从后端传入的数据
          loadNode(node, resolve) {
            if (node.level === 0) {
              return resolve([{ name: 'region1' }, { name: 'region2' }]);
            }
            if (node.level > 3) return resolve([]);

            var hasChild;
            if (node.data.name === 'region1') {
              hasChild = true;
            } else if (node.data.name === 'region2') {
              hasChild = false;
            } else {
              hasChild = Math.random() > 0.5;
            }

            setTimeout(() => {
              var data;
              if (hasChild) {
                data = [{
                  name: 'zone' + this.count++
                }, {
                  name: 'zone' + this.count++
                }];
              } else {
                data = [];
              }

              resolve(data);
            }, 500);
          }
        }
      };
    </script>







