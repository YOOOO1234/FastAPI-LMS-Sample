<template>
    <v-container>
        <v-row align="center" justify="space-around" >
            <v-text-field :rules="email_rules" label="email" v-model="email"></v-text-field>
        </v-row>
        <v-row align="center" justify="space-around" >
            <v-text-field 
            :append-icon="pswd ? 'mdi-eye' : 'mdi-eye-off'"
            :rules="password_rules" 
            :type="pswd ? 'text' : 'password'"
            label="password" 
            class="input-group--focused"
            @click:append="pswd = !pswd"
            v-model="password"
            ></v-text-field>
        </v-row>
        <v-row align="center" justify="space-around" >
          <div v-if="fale_cnt<5">
            <v-btn depressed color="primary" @click="login()" value="POST">
                ログイン
            </v-btn>
          </div>
          <div :class="`rounded-lg`" class="pa-6 mt-6 red lighten-5 text-no-wrap"  v-else>
            ５回入力に失敗したので時間を空けてログインしてください。
          </div>
        </v-row>
    </v-container>
</template>

<script>
import axios from "axios";
export default {
  
  name: "Login",
  data: () => ({
      pswd: false,
      email: "neo@neo.com",
      password: "neoneo",
      fale_cnt: 0,
      email_rules: [
        value => !!value || 'メールアドレスを入力してください.',
      ],
      password_rules: [
        value => !!value || 'パスワードを入力してください',
      ]
    }),
  methods:{
      login: function(){
        console.log(this.email,this.password)
        const config = {
          headers: {
            'Content-Type': 'application/json'
          },
          withCredentials: true
        };
        const params = {email: this.email,password: this.password}
        let self = this
        axios.post("http://localhost:8000/token", params, config)
        .then(function(response){
          console.log(response.data)
          axios.get("http://localhost:8000/home_profile", {withCredentials: true})
          .then(function(response){
              if(response.data.create){
                self.go_teacher_home()
              }else{
                self.go_students_home()
              }
          }).catch(
            function(error)  {
              console.log(error)
              if(error.response.status == 401){
                self.$router.push({name:'Signup'})
              }else{
                console.log(error.response)
              }
            }
          )}
        ).catch(
          function(error){
            self.fale_cnt +=1
            alert('ログインに失敗しました。正しいメールアドレス・パスワードを入力してください');
            console.log(error)
          }
        )
      },
      go_signup_page: function(){
          this.$router.push({name:'Signup'})
      },
      go_students_home: function(){
          this.$router.push({name:'StudentHome'})
      },
      go_teacher_home: function(){
          this.$router.push({name:'TeacherHome'})
      },

  },
};
</script>
