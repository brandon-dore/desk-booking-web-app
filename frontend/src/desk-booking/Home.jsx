import React, { useEffect, useState } from 'react';
import TopBar from '../auth/TopBar';
import UserService from '../services/user.service';


const Home = () => {

     const [user, setUser] = useState(undefined)

     useEffect(() => {
          UserService.getUserInfo().then(
               response => {
                    setUser(response.data)
               },
               error => {
                 console.log(error);
               }
             );
     }, [])

     return (
          <>
               <TopBar />
               <h1>
                    test = {JSON.stringify(user)}
               </h1>
          </>
     )
}

export default Home;