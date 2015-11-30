/*
 *  Licensed to the Apache Software Foundation (ASF) under one or more
 *  contributor license agreements.  See the NOTICE file distributed with
 *  this work for additional information regarding copyright ownership.
 *  The ASF licenses this file to You under the Apache License, Version 2.0
 *  (the "License"); you may not use this file except in compliance with
 *  the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

/***************************************************************************
 * Description: Platform specific, auto-detected types.                    *
 * Author:      Rainer Jung <rjung@apache.org>                             *
 * Version:     $Revision: 915199 $                                           *
 ***************************************************************************/

#ifndef JK_TYPES_H
#define JK_TYPES_H

/* GENERATED FILE WARNING!  DO NOT EDIT jk_types.h
 *
 * You must modify jk_types.h.in instead.
 *
 */

#ifdef __cplusplus
extern "C"
{
#endif                          /* __cplusplus */

/* jk_uint32_t defines a four byte word */
typedef unsigned int jk_uint32_t;

/* And JK_UINT32_T_FMT */
#define JK_UINT32_T_FMT "u"

/* And JK_UINT32_T_HEX_FMT */
#define JK_UINT32_T_HEX_FMT "x"

/* jk_uint64_t defines a eight byte word */
typedef unsigned long jk_uint64_t;

/* And JK_UINT64_T_FMT */
#define JK_UINT64_T_FMT "lu"

/* And JK_UINT64_T_HEX_FMT */
#define JK_UINT64_T_HEX_FMT "lx"

/* And JK_PID_T_FMT */
#define JK_PID_T_FMT "d"

/* jk_pthread_t defines a eight byte word */
typedef unsigned long jk_pthread_t;

/* And JK_PTHREAD_T_FMT */
#define JK_PTHREAD_T_FMT "lu"

#ifdef __cplusplus
}
#endif                          /* __cplusplus */

#endif                          /* JK_TYPES_H */
