/******************************************************************************* 
 * Copyright (c) 2016 HUAWEI TECHNOLOGIES CO.,LTD and others. 
 *
 * All rights reserved. This program and the accompanying materials 
 * are made available under the terms of the Apache License, Version 2.0 
 * which accompanies this distribution, and is available at 
 * http://www.apache.org/licenses/LICENSE-2.0 
 *******************************************************************************/ 
package edu.rice.rubbos.servlets;

public class Config
{

  /**
   * Creates a new <code>Config</code> instance.
   */
  Config()
  {
  }


  public static final String HTMLFilesPath                 = "/bottlenecks/rubbos/app/RUBBoS/Servlet_HTML";
  public static final String[] DatabaseProperties          = {"/bottlenecks/rubbos/app/RUBBoS/Servlets/mysql.properties"};
  public static final int DatabasePropertiesSize = 1;

  public static final int    AboutMePoolSize               = 10;
  public static final int    BrowseCategoriesPoolSize      = 6;
  public static final int    BrowseRegionsPoolSize         = 6;
  public static final int    BuyNowPoolSize                = 4;
  public static final int    PutBidPoolSize                = 8;
  public static final int    PutCommentPoolSize            = 2;
  public static final int    RegisterItemPoolSize          = 2;
  public static final int    RegisterUserPoolSize          = 2;
  public static final int    SearchItemsByCategoryPoolSize = 15;
  public static final int    SearchItemsByRegionPoolSize   = 20;
  public static final int    StoreBidPoolSize              = 8;
  public static final int    StoreBuyNowPoolSize           = 4;
  public static final int    StoreCommentPoolSize          = 2;
  public static final int    ViewBidHistoryPoolSize        = 4;
  public static final int    ViewItemPoolSize              = 20;
  public static final int    ViewUserInfoPoolSize          = 4;
}
