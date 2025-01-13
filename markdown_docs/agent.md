Skip to content

[ ![logo](../../img/logo-white.svg) ](../.. "PydanticAI")

PydanticAI

pydantic_ai.Agent

Type to start searching

[ pydantic/pydantic-ai

  * v0.0.14
  * 4.2k
  * 255

](https://github.com/pydantic/pydantic-ai "Go to repository")

[ ![logo](../../img/logo-white.svg) ](../.. "PydanticAI") PydanticAI

[ pydantic/pydantic-ai

  * v0.0.14
  * 4.2k
  * 255

](https://github.com/pydantic/pydantic-ai "Go to repository")

  * [ Introduction  ](../..)
  * [ Installation  ](../../install/)
  * [ Getting Help  ](../../help/)
  * [ Contributing  ](../../contributing/)
  * Documentation  Documentation 
    * [ Agents  ](../../agents/)
    * [ Models  ](../../models/)
    * [ Dependencies  ](../../dependencies/)
    * [ Function Tools  ](../../tools/)
    * [ Results  ](../../results/)
    * [ Messages and chat history  ](../../message-history/)
    * [ Testing and Evals  ](../../testing-evals/)
    * [ Debugging and Monitoring  ](../../logfire/)
  * [ Examples  ](../../examples/)

Examples

    * [ Pydantic Model  ](../../examples/pydantic-model/)
    * [ Weather agent  ](../../examples/weather-agent/)
    * [ Bank support  ](../../examples/bank-support/)
    * [ SQL Generation  ](../../examples/sql-gen/)
    * [ RAG  ](../../examples/rag/)
    * [ Stream markdown  ](../../examples/stream-markdown/)
    * [ Stream whales  ](../../examples/stream-whales/)
    * [ Chat App with FastAPI  ](../../examples/chat-app/)
  * API Reference  API Reference 
    * pydantic_ai.Agent  [ pydantic_ai.Agent  ](./) Table of contents 
      * Agent 
      * __init__ 
      * name 
      * run 
      * run_sync 
      * run_stream 
      * model 
      * override 
      * last_run_messages 
      * system_prompt 
      * tool 
      * tool_plain 
      * result_validator 
      * EndStrategy 
    * [ pydantic_ai.tools  ](../tools/)
    * [ pydantic_ai.result  ](../result/)
    * [ pydantic_ai.messages  ](../messages/)
    * [ pydantic_ai.exceptions  ](../exceptions/)
    * [ pydantic_ai.settings  ](../settings/)
    * [ pydantic_ai.models  ](../models/base/)
    * [ pydantic_ai.models.openai  ](../models/openai/)
    * [ pydantic_ai.models.anthropic  ](../models/anthropic/)
    * [ pydantic_ai.models.gemini  ](../models/gemini/)
    * [ pydantic_ai.models.vertexai  ](../models/vertexai/)
    * [ pydantic_ai.models.groq  ](../models/groq/)
    * [ pydantic_ai.models.mistral  ](../models/mistral/)
    * [ pydantic_ai.models.ollama  ](../models/ollama/)
    * [ pydantic_ai.models.test  ](../models/test/)
    * [ pydantic_ai.models.function  ](../models/function/)

Table of contents

  * Agent 
  * __init__ 
  * name 
  * run 
  * run_sync 
  * run_stream 
  * model 
  * override 
  * last_run_messages 
  * system_prompt 
  * tool 
  * tool_plain 
  * result_validator 
  * EndStrategy 

  1. [ Introduction  ](../..)
  2. [ API Reference  ](./)

# `pydantic_ai.Agent`

Bases: `[Generic](https://docs.python.org/3/library/typing.html#typing.Generic
"typing.Generic")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps
"pydantic_ai.tools.AgentDeps"),
[ResultData](../result/#pydantic_ai.result.ResultData
"pydantic_ai.result.ResultData")]`

Class for defining "agents" - a way to have a specific type of "conversation"
with an LLM.

Agents are generic in the dependency type they take
[`AgentDeps`](../tools/#pydantic_ai.tools.AgentDeps) and the result data type
they return, [`ResultData`](../result/#pydantic_ai.result.ResultData).

By default, if neither generic parameter is customised, agents have type
`Agent[None, str]`.

Minimal usage example:

    
    
    from pydantic_ai import Agent
    
    agent = Agent('openai:gpt-4o')
    result = agent.run_sync('What is the capital of France?')
    print(result.data)
    #> Paris
    

Source code in `pydantic_ai_slim/pydantic_ai/agent.py`

    
    
      51
      52
      53
      54
      55
      56
      57
      58
      59
      60
      61
      62
      63
      64
      65
      66
      67
      68
      69
      70
      71
      72
      73
      74
      75
      76
      77
      78
      79
      80
      81
      82
      83
      84
      85
      86
      87
      88
      89
      90
      91
      92
      93
      94
      95
      96
      97
      98
      99
     100
     101
     102
     103
     104
     105
     106
     107
     108
     109
     110
     111
     112
     113
     114
     115
     116
     117
     118
     119
     120
     121
     122
     123
     124
     125
     126
     127
     128
     129
     130
     131
     132
     133
     134
     135
     136
     137
     138
     139
     140
     141
     142
     143
     144
     145
     146
     147
     148
     149
     150
     151
     152
     153
     154
     155
     156
     157
     158
     159
     160
     161
     162
     163
     164
     165
     166
     167
     168
     169
     170
     171
     172
     173
     174
     175
     176
     177
     178
     179
     180
     181
     182
     183
     184
     185
     186
     187
     188
     189
     190
     191
     192
     193
     194
     195
     196
     197
     198
     199
     200
     201
     202
     203
     204
     205
     206
     207
     208
     209
     210
     211
     212
     213
     214
     215
     216
     217
     218
     219
     220
     221
     222
     223
     224
     225
     226
     227
     228
     229
     230
     231
     232
     233
     234
     235
     236
     237
     238
     239
     240
     241
     242
     243
     244
     245
     246
     247
     248
     249
     250
     251
     252
     253
     254
     255
     256
     257
     258
     259
     260
     261
     262
     263
     264
     265
     266
     267
     268
     269
     270
     271
     272
     273
     274
     275
     276
     277
     278
     279
     280
     281
     282
     283
     284
     285
     286
     287
     288
     289
     290
     291
     292
     293
     294
     295
     296
     297
     298
     299
     300
     301
     302
     303
     304
     305
     306
     307
     308
     309
     310
     311
     312
     313
     314
     315
     316
     317
     318
     319
     320
     321
     322
     323
     324
     325
     326
     327
     328
     329
     330
     331
     332
     333
     334
     335
     336
     337
     338
     339
     340
     341
     342
     343
     344
     345
     346
     347
     348
     349
     350
     351
     352
     353
     354
     355
     356
     357
     358
     359
     360
     361
     362
     363
     364
     365
     366
     367
     368
     369
     370
     371
     372
     373
     374
     375
     376
     377
     378
     379
     380
     381
     382
     383
     384
     385
     386
     387
     388
     389
     390
     391
     392
     393
     394
     395
     396
     397
     398
     399
     400
     401
     402
     403
     404
     405
     406
     407
     408
     409
     410
     411
     412
     413
     414
     415
     416
     417
     418
     419
     420
     421
     422
     423
     424
     425
     426
     427
     428
     429
     430
     431
     432
     433
     434
     435
     436
     437
     438
     439
     440
     441
     442
     443
     444
     445
     446
     447
     448
     449
     450
     451
     452
     453
     454
     455
     456
     457
     458
     459
     460
     461
     462
     463
     464
     465
     466
     467
     468
     469
     470
     471
     472
     473
     474
     475
     476
     477
     478
     479
     480
     481
     482
     483
     484
     485
     486
     487
     488
     489
     490
     491
     492
     493
     494
     495
     496
     497
     498
     499
     500
     501
     502
     503
     504
     505
     506
     507
     508
     509
     510
     511
     512
     513
     514
     515
     516
     517
     518
     519
     520
     521
     522
     523
     524
     525
     526
     527
     528
     529
     530
     531
     532
     533
     534
     535
     536
     537
     538
     539
     540
     541
     542
     543
     544
     545
     546
     547
     548
     549
     550
     551
     552
     553
     554
     555
     556
     557
     558
     559
     560
     561
     562
     563
     564
     565
     566
     567
     568
     569
     570
     571
     572
     573
     574
     575
     576
     577
     578
     579
     580
     581
     582
     583
     584
     585
     586
     587
     588
     589
     590
     591
     592
     593
     594
     595
     596
     597
     598
     599
     600
     601
     602
     603
     604
     605
     606
     607
     608
     609
     610
     611
     612
     613
     614
     615
     616
     617
     618
     619
     620
     621
     622
     623
     624
     625
     626
     627
     628
     629
     630
     631
     632
     633
     634
     635
     636
     637
     638
     639
     640
     641
     642
     643
     644
     645
     646
     647
     648
     649
     650
     651
     652
     653
     654
     655
     656
     657
     658
     659
     660
     661
     662
     663
     664
     665
     666
     667
     668
     669
     670
     671
     672
     673
     674
     675
     676
     677
     678
     679
     680
     681
     682
     683
     684
     685
     686
     687
     688
     689
     690
     691
     692
     693
     694
     695
     696
     697
     698
     699
     700
     701
     702
     703
     704
     705
     706
     707
     708
     709
     710
     711
     712
     713
     714
     715
     716
     717
     718
     719
     720
     721
     722
     723
     724
     725
     726
     727
     728
     729
     730
     731
     732
     733
     734
     735
     736
     737
     738
     739
     740
     741
     742
     743
     744
     745
     746
     747
     748
     749
     750
     751
     752
     753
     754
     755
     756
     757
     758
     759
     760
     761
     762
     763
     764
     765
     766
     767
     768
     769
     770
     771
     772
     773
     774
     775
     776
     777
     778
     779
     780
     781
     782
     783
     784
     785
     786
     787
     788
     789
     790
     791
     792
     793
     794
     795
     796
     797
     798
     799
     800
     801
     802
     803
     804
     805
     806
     807
     808
     809
     810
     811
     812
     813
     814
     815
     816
     817
     818
     819
     820
     821
     822
     823
     824
     825
     826
     827
     828
     829
     830
     831
     832
     833
     834
     835
     836
     837
     838
     839
     840
     841
     842
     843
     844
     845
     846
     847
     848
     849
     850
     851
     852
     853
     854
     855
     856
     857
     858
     859
     860
     861
     862
     863
     864
     865
     866
     867
     868
     869
     870
     871
     872
     873
     874
     875
     876
     877
     878
     879
     880
     881
     882
     883
     884
     885
     886
     887
     888
     889
     890
     891
     892
     893
     894
     895
     896
     897
     898
     899
     900
     901
     902
     903
     904
     905
     906
     907
     908
     909
     910
     911
     912
     913
     914
     915
     916
     917
     918
     919
     920
     921
     922
     923
     924
     925
     926
     927
     928
     929
     930
     931
     932
     933
     934
     935
     936
     937
     938
     939
     940
     941
     942
     943
     944
     945
     946
     947
     948
     949
     950
     951
     952
     953
     954
     955
     956
     957
     958
     959
     960
     961
     962
     963
     964
     965
     966
     967
     968
     969
     970
     971
     972
     973
     974
     975
     976
     977
     978
     979
     980
     981
     982
     983
     984
     985
     986
     987
     988
     989
     990
     991
     992
     993
     994
     995
     996
     997
     998
     999
    1000
    1001
    1002
    1003
    1004
    1005
    1006
    1007
    1008
    1009
    1010
    1011
    1012
    1013
    1014
    1015
    1016
    1017
    1018
    1019
    1020
    1021
    1022
    1023
    1024
    1025
    1026
    1027
    1028
    1029
    1030
    1031
    1032
    1033
    1034
    1035
    1036
    1037
    1038
    1039
    1040
    1041
    1042
    1043
    1044
    1045
    1046
    1047
    1048
    1049
    1050
    1051
    1052
    1053
    1054
    1055
    1056
    1057
    1058
    1059
    1060
    1061
    1062
    1063
    1064
    1065
    1066
    1067
    1068
    1069
    1070
    1071
    1072
    1073
    1074
    1075
    1076
    1077
    1078
    1079
    1080
    1081
    1082
    1083
    1084
    1085
    1086
    1087
    1088
    1089
    1090
    1091
    1092
    1093
    1094
    1095
    1096
    1097
    1098
    1099
    1100
    1101
    1102
    1103
    1104
    1105
    1106
    1107
    1108
    1109
    1110
    1111
    1112
    1113
    1114
    1115
    1116
    1117
    1118
    1119
    1120

|

    
    
    @final
    @dataclass(init=False)
    class Agent(Generic[AgentDeps, ResultData]):
        """Class for defining "agents" - a way to have a specific type of "conversation" with an LLM.
    
        Agents are generic in the dependency type they take [`AgentDeps`][pydantic_ai.tools.AgentDeps]
        and the result data type they return, [`ResultData`][pydantic_ai.result.ResultData].
    
        By default, if neither generic parameter is customised, agents have type `Agent[None, str]`.
    
        Minimal usage example:
    
        ```python
        from pydantic_ai import Agent
    
        agent = Agent('openai:gpt-4o')
        result = agent.run_sync('What is the capital of France?')
        print(result.data)
        #> Paris
        ```
        """
    
        # we use dataclass fields in order to conveniently know what attributes are available
        model: models.Model | models.KnownModelName | None
        """The default model configured for this agent."""
    
        name: str | None
        """The name of the agent, used for logging.
    
        If `None`, we try to infer the agent name from the call frame when the agent is first run.
        """
        end_strategy: EndStrategy
        """Strategy for handling tool calls when a final result is found."""
    
        model_settings: ModelSettings | None
        """Optional model request settings to use for this agents's runs, by default.
    
        Note, if `model_settings` is provided by `run`, `run_sync`, or `run_stream`, those settings will
        be merged with this value, with the runtime argument taking priority.
        """
    
        last_run_messages: list[_messages.ModelMessage] | None
        """The messages from the last run, useful when a run raised an exception.
    
        Note: these are not used by the agent, e.g. in future runs, they are just stored for developers' convenience.
        """
    
        _result_schema: _result.ResultSchema[ResultData] | None = field(repr=False)
        _result_validators: list[_result.ResultValidator[AgentDeps, ResultData]] = field(repr=False)
        _allow_text_result: bool = field(repr=False)
        _system_prompts: tuple[str, ...] = field(repr=False)
        _function_tools: dict[str, Tool[AgentDeps]] = field(repr=False)
        _default_retries: int = field(repr=False)
        _system_prompt_functions: list[_system_prompt.SystemPromptRunner[AgentDeps]] = field(repr=False)
        _deps_type: type[AgentDeps] = field(repr=False)
        _max_result_retries: int = field(repr=False)
        _override_deps: _utils.Option[AgentDeps] = field(default=None, repr=False)
        _override_model: _utils.Option[models.Model] = field(default=None, repr=False)
    
        def __init__(
            self,
            model: models.Model | models.KnownModelName | None = None,
            *,
            result_type: type[ResultData] = str,
            system_prompt: str | Sequence[str] = (),
            deps_type: type[AgentDeps] = NoneType,
            name: str | None = None,
            model_settings: ModelSettings | None = None,
            retries: int = 1,
            result_tool_name: str = 'final_result',
            result_tool_description: str | None = None,
            result_retries: int | None = None,
            tools: Sequence[Tool[AgentDeps] | ToolFuncEither[AgentDeps, ...]] = (),
            defer_model_check: bool = False,
            end_strategy: EndStrategy = 'early',
        ):
            """Create an agent.
    
            Args:
                model: The default model to use for this agent, if not provide,
                    you must provide the model when calling it.
                result_type: The type of the result data, used to validate the result data, defaults to `str`.
                system_prompt: Static system prompts to use for this agent, you can also register system
                    prompts via a function with [`system_prompt`][pydantic_ai.Agent.system_prompt].
                deps_type: The type used for dependency injection, this parameter exists solely to allow you to fully
                    parameterize the agent, and therefore get the best out of static type checking.
                    If you're not using deps, but want type checking to pass, you can set `deps=None` to satisfy Pyright
                    or add a type hint `: Agent[None, <return type>]`.
                name: The name of the agent, used for logging. If `None`, we try to infer the agent name from the call frame
                    when the agent is first run.
                model_settings: Optional model request settings to use for this agent's runs, by default.
                retries: The default number of retries to allow before raising an error.
                result_tool_name: The name of the tool to use for the final result.
                result_tool_description: The description of the final result tool.
                result_retries: The maximum number of retries to allow for result validation, defaults to `retries`.
                tools: Tools to register with the agent, you can also register tools via the decorators
                    [`@agent.tool`][pydantic_ai.Agent.tool] and [`@agent.tool_plain`][pydantic_ai.Agent.tool_plain].
                defer_model_check: by default, if you provide a [named][pydantic_ai.models.KnownModelName] model,
                    it's evaluated to create a [`Model`][pydantic_ai.models.Model] instance immediately,
                    which checks for the necessary environment variables. Set this to `false`
                    to defer the evaluation until the first run. Useful if you want to
                    [override the model][pydantic_ai.Agent.override] for testing.
                end_strategy: Strategy for handling tool calls that are requested alongside a final result.
                    See [`EndStrategy`][pydantic_ai.agent.EndStrategy] for more information.
            """
            if model is None or defer_model_check:
                self.model = model
            else:
                self.model = models.infer_model(model)
    
            self.end_strategy = end_strategy
            self.name = name
            self.model_settings = model_settings
            self.last_run_messages = None
            self._result_schema = _result.ResultSchema[result_type].build(
                result_type, result_tool_name, result_tool_description
            )
            # if the result tool is None, or its schema allows `str`, we allow plain text results
            self._allow_text_result = self._result_schema is None or self._result_schema.allow_text_result
    
            self._system_prompts = (system_prompt,) if isinstance(system_prompt, str) else tuple(system_prompt)
            self._function_tools = {}
            self._default_retries = retries
            for tool in tools:
                if isinstance(tool, Tool):
                    self._register_tool(tool)
                else:
                    self._register_tool(Tool(tool))
            self._deps_type = deps_type
            self._system_prompt_functions = []
            self._max_result_retries = result_retries if result_retries is not None else retries
            self._result_validators = []
    
        async def run(
            self,
            user_prompt: str,
            *,
            message_history: list[_messages.ModelMessage] | None = None,
            model: models.Model | models.KnownModelName | None = None,
            deps: AgentDeps = None,
            model_settings: ModelSettings | None = None,
            usage_limits: UsageLimits | None = None,
            infer_name: bool = True,
        ) -> result.RunResult[ResultData]:
            """Run the agent with a user prompt in async mode.
    
            Example:
            ```python
            from pydantic_ai import Agent
    
            agent = Agent('openai:gpt-4o')
    
            result_sync = agent.run_sync('What is the capital of Italy?')
            print(result_sync.data)
            #> Rome
            ```
    
            Args:
                user_prompt: User input to start/continue the conversation.
                message_history: History of the conversation so far.
                model: Optional model to use for this run, required if `model` was not set when creating the agent.
                deps: Optional dependencies to use for this run.
                model_settings: Optional settings to use for this model's request.
                usage_limits: Optional limits on model request count or token usage.
                infer_name: Whether to try to infer the agent name from the call frame if it's not set.
    
            Returns:
                The result of the run.
            """
            if infer_name and self.name is None:
                self._infer_name(inspect.currentframe())
            model_used, mode_selection = await self._get_model(model)
    
            deps = self._get_deps(deps)
            new_message_index = len(message_history) if message_history else 0
    
            with _logfire.span(
                '{agent_name} run {prompt=}',
                prompt=user_prompt,
                agent=self,
                mode_selection=mode_selection,
                model_name=model_used.name(),
                agent_name=self.name or 'agent',
            ) as run_span:
                run_context = RunContext(deps, 0, [], None, model_used)
                messages = await self._prepare_messages(user_prompt, message_history, run_context)
                self.last_run_messages = run_context.messages = messages
    
                for tool in self._function_tools.values():
                    tool.current_retry = 0
    
                usage = result.Usage(requests=0)
                model_settings = merge_model_settings(self.model_settings, model_settings)
                usage_limits = usage_limits or UsageLimits()
    
                run_step = 0
                while True:
                    usage_limits.check_before_request(usage)
    
                    run_step += 1
                    with _logfire.span('preparing model and tools {run_step=}', run_step=run_step):
                        agent_model = await self._prepare_model(run_context)
    
                    with _logfire.span('model request', run_step=run_step) as model_req_span:
                        model_response, request_usage = await agent_model.request(messages, model_settings)
                        model_req_span.set_attribute('response', model_response)
                        model_req_span.set_attribute('usage', request_usage)
    
                    messages.append(model_response)
                    usage += request_usage
                    usage.requests += 1
                    usage_limits.check_tokens(request_usage)
    
                    with _logfire.span('handle model response', run_step=run_step) as handle_span:
                        final_result, tool_responses = await self._handle_model_response(model_response, run_context)
    
                        if tool_responses:
                            # Add parts to the conversation as a new message
                            messages.append(_messages.ModelRequest(tool_responses))
    
                        # Check if we got a final result
                        if final_result is not None:
                            result_data = final_result.data
                            run_span.set_attribute('all_messages', messages)
                            run_span.set_attribute('usage', usage)
                            handle_span.set_attribute('result', result_data)
                            handle_span.message = 'handle model response -> final result'
                            return result.RunResult(messages, new_message_index, result_data, usage)
                        else:
                            # continue the conversation
                            handle_span.set_attribute('tool_responses', tool_responses)
                            tool_responses_str = ' '.join(r.part_kind for r in tool_responses)
                            handle_span.message = f'handle model response -> {tool_responses_str}'
    
        def run_sync(
            self,
            user_prompt: str,
            *,
            message_history: list[_messages.ModelMessage] | None = None,
            model: models.Model | models.KnownModelName | None = None,
            deps: AgentDeps = None,
            model_settings: ModelSettings | None = None,
            usage_limits: UsageLimits | None = None,
            infer_name: bool = True,
        ) -> result.RunResult[ResultData]:
            """Run the agent with a user prompt synchronously.
    
            This is a convenience method that wraps [`self.run`][pydantic_ai.Agent.run] with `loop.run_until_complete(...)`.
            You therefore can't use this method inside async code or if there's an active event loop.
    
            Example:
            ```python
            from pydantic_ai import Agent
    
            agent = Agent('openai:gpt-4o')
    
            async def main():
                result = await agent.run('What is the capital of France?')
                print(result.data)
                #> Paris
            ```
    
            Args:
                user_prompt: User input to start/continue the conversation.
                message_history: History of the conversation so far.
                model: Optional model to use for this run, required if `model` was not set when creating the agent.
                deps: Optional dependencies to use for this run.
                model_settings: Optional settings to use for this model's request.
                usage_limits: Optional limits on model request count or token usage.
                infer_name: Whether to try to infer the agent name from the call frame if it's not set.
    
            Returns:
                The result of the run.
            """
            if infer_name and self.name is None:
                self._infer_name(inspect.currentframe())
            return asyncio.get_event_loop().run_until_complete(
                self.run(
                    user_prompt,
                    message_history=message_history,
                    model=model,
                    deps=deps,
                    model_settings=model_settings,
                    usage_limits=usage_limits,
                    infer_name=False,
                )
            )
    
        @asynccontextmanager
        async def run_stream(
            self,
            user_prompt: str,
            *,
            message_history: list[_messages.ModelMessage] | None = None,
            model: models.Model | models.KnownModelName | None = None,
            deps: AgentDeps = None,
            model_settings: ModelSettings | None = None,
            usage_limits: UsageLimits | None = None,
            infer_name: bool = True,
        ) -> AsyncIterator[result.StreamedRunResult[AgentDeps, ResultData]]:
            """Run the agent with a user prompt in async mode, returning a streamed response.
    
            Example:
            ```python
            from pydantic_ai import Agent
    
            agent = Agent('openai:gpt-4o')
    
            async def main():
                async with agent.run_stream('What is the capital of the UK?') as response:
                    print(await response.get_data())
                    #> London
            ```
    
            Args:
                user_prompt: User input to start/continue the conversation.
                message_history: History of the conversation so far.
                model: Optional model to use for this run, required if `model` was not set when creating the agent.
                deps: Optional dependencies to use for this run.
                model_settings: Optional settings to use for this model's request.
                usage_limits: Optional limits on model request count or token usage.
                infer_name: Whether to try to infer the agent name from the call frame if it's not set.
    
            Returns:
                The result of the run.
            """
            if infer_name and self.name is None:
                # f_back because `asynccontextmanager` adds one frame
                if frame := inspect.currentframe():  # pragma: no branch
                    self._infer_name(frame.f_back)
            model_used, mode_selection = await self._get_model(model)
    
            deps = self._get_deps(deps)
            new_message_index = len(message_history) if message_history else 0
    
            with _logfire.span(
                '{agent_name} run stream {prompt=}',
                prompt=user_prompt,
                agent=self,
                mode_selection=mode_selection,
                model_name=model_used.name(),
                agent_name=self.name or 'agent',
            ) as run_span:
                run_context = RunContext(deps, 0, [], None, model_used)
                messages = await self._prepare_messages(user_prompt, message_history, run_context)
                self.last_run_messages = run_context.messages = messages
    
                for tool in self._function_tools.values():
                    tool.current_retry = 0
    
                usage = result.Usage()
                model_settings = merge_model_settings(self.model_settings, model_settings)
                usage_limits = usage_limits or UsageLimits()
    
                run_step = 0
                while True:
                    run_step += 1
                    usage_limits.check_before_request(usage)
    
                    with _logfire.span('preparing model and tools {run_step=}', run_step=run_step):
                        agent_model = await self._prepare_model(run_context)
    
                    with _logfire.span('model request {run_step=}', run_step=run_step) as model_req_span:
                        async with agent_model.request_stream(messages, model_settings) as model_response:
                            usage.requests += 1
                            model_req_span.set_attribute('response_type', model_response.__class__.__name__)
                            # We want to end the "model request" span here, but we can't exit the context manager
                            # in the traditional way
                            model_req_span.__exit__(None, None, None)
    
                            with _logfire.span('handle model response') as handle_span:
                                maybe_final_result = await self._handle_streamed_model_response(model_response, run_context)
    
                                # Check if we got a final result
                                if isinstance(maybe_final_result, _MarkFinalResult):
                                    result_stream = maybe_final_result.data
                                    result_tool_name = maybe_final_result.tool_name
                                    handle_span.message = 'handle model response -> final result'
    
                                    async def on_complete():
                                        """Called when the stream has completed.
    
                                        The model response will have been added to messages by now
                                        by `StreamedRunResult._marked_completed`.
                                        """
                                        last_message = messages[-1]
                                        assert isinstance(last_message, _messages.ModelResponse)
                                        tool_calls = [
                                            part for part in last_message.parts if isinstance(part, _messages.ToolCallPart)
                                        ]
                                        parts = await self._process_function_tools(
                                            tool_calls, result_tool_name, run_context
                                        )
                                        if parts:
                                            messages.append(_messages.ModelRequest(parts))
                                        run_span.set_attribute('all_messages', messages)
    
                                    yield result.StreamedRunResult(
                                        messages,
                                        new_message_index,
                                        usage,
                                        usage_limits,
                                        result_stream,
                                        self._result_schema,
                                        run_context,
                                        self._result_validators,
                                        result_tool_name,
                                        on_complete,
                                    )
                                    return
                                else:
                                    # continue the conversation
                                    model_response_msg, tool_responses = maybe_final_result
                                    # if we got a model response add that to messages
                                    messages.append(model_response_msg)
                                    if tool_responses:
                                        # if we got one or more tool response parts, add a model request message
                                        messages.append(_messages.ModelRequest(tool_responses))
    
                                    handle_span.set_attribute('tool_responses', tool_responses)
                                    tool_responses_str = ' '.join(r.part_kind for r in tool_responses)
                                    handle_span.message = f'handle model response -> {tool_responses_str}'
                                    # the model_response should have been fully streamed by now, we can add its usage
                                    model_response_usage = model_response.usage()
                                    usage += model_response_usage
                                    usage_limits.check_tokens(usage)
    
        @contextmanager
        def override(
            self,
            *,
            deps: AgentDeps | _utils.Unset = _utils.UNSET,
            model: models.Model | models.KnownModelName | _utils.Unset = _utils.UNSET,
        ) -> Iterator[None]:
            """Context manager to temporarily override agent dependencies and model.
    
            This is particularly useful when testing.
            You can find an example of this [here](../testing-evals.md#overriding-model-via-pytest-fixtures).
    
            Args:
                deps: The dependencies to use instead of the dependencies passed to the agent run.
                model: The model to use instead of the model passed to the agent run.
            """
            if _utils.is_set(deps):
                override_deps_before = self._override_deps
                self._override_deps = _utils.Some(deps)
            else:
                override_deps_before = _utils.UNSET
    
            # noinspection PyTypeChecker
            if _utils.is_set(model):
                override_model_before = self._override_model
                # noinspection PyTypeChecker
                self._override_model = _utils.Some(models.infer_model(model))  # pyright: ignore[reportArgumentType]
            else:
                override_model_before = _utils.UNSET
    
            try:
                yield
            finally:
                if _utils.is_set(override_deps_before):
                    self._override_deps = override_deps_before
                if _utils.is_set(override_model_before):
                    self._override_model = override_model_before
    
        @overload
        def system_prompt(
            self, func: Callable[[RunContext[AgentDeps]], str], /
        ) -> Callable[[RunContext[AgentDeps]], str]: ...
    
        @overload
        def system_prompt(
            self, func: Callable[[RunContext[AgentDeps]], Awaitable[str]], /
        ) -> Callable[[RunContext[AgentDeps]], Awaitable[str]]: ...
    
        @overload
        def system_prompt(self, func: Callable[[], str], /) -> Callable[[], str]: ...
    
        @overload
        def system_prompt(self, func: Callable[[], Awaitable[str]], /) -> Callable[[], Awaitable[str]]: ...
    
        def system_prompt(
            self, func: _system_prompt.SystemPromptFunc[AgentDeps], /
        ) -> _system_prompt.SystemPromptFunc[AgentDeps]:
            """Decorator to register a system prompt function.
    
            Optionally takes [`RunContext`][pydantic_ai.tools.RunContext] as its only argument.
            Can decorate a sync or async functions.
    
            Overloads for every possible signature of `system_prompt` are included so the decorator doesn't obscure
            the type of the function, see `tests/typed_agent.py` for tests.
    
            Example:
            ```python
            from pydantic_ai import Agent, RunContext
    
            agent = Agent('test', deps_type=str)
    
            @agent.system_prompt
            def simple_system_prompt() -> str:
                return 'foobar'
    
            @agent.system_prompt
            async def async_system_prompt(ctx: RunContext[str]) -> str:
                return f'{ctx.deps} is the best'
    
            result = agent.run_sync('foobar', deps='spam')
            print(result.data)
            #> success (no tool calls)
            ```
            """
            self._system_prompt_functions.append(_system_prompt.SystemPromptRunner(func))
            return func
    
        @overload
        def result_validator(
            self, func: Callable[[RunContext[AgentDeps], ResultData], ResultData], /
        ) -> Callable[[RunContext[AgentDeps], ResultData], ResultData]: ...
    
        @overload
        def result_validator(
            self, func: Callable[[RunContext[AgentDeps], ResultData], Awaitable[ResultData]], /
        ) -> Callable[[RunContext[AgentDeps], ResultData], Awaitable[ResultData]]: ...
    
        @overload
        def result_validator(self, func: Callable[[ResultData], ResultData], /) -> Callable[[ResultData], ResultData]: ...
    
        @overload
        def result_validator(
            self, func: Callable[[ResultData], Awaitable[ResultData]], /
        ) -> Callable[[ResultData], Awaitable[ResultData]]: ...
    
        def result_validator(
            self, func: _result.ResultValidatorFunc[AgentDeps, ResultData], /
        ) -> _result.ResultValidatorFunc[AgentDeps, ResultData]:
            """Decorator to register a result validator function.
    
            Optionally takes [`RunContext`][pydantic_ai.tools.RunContext] as its first argument.
            Can decorate a sync or async functions.
    
            Overloads for every possible signature of `result_validator` are included so the decorator doesn't obscure
            the type of the function, see `tests/typed_agent.py` for tests.
    
            Example:
            ```python
            from pydantic_ai import Agent, ModelRetry, RunContext
    
            agent = Agent('test', deps_type=str)
    
            @agent.result_validator
            def result_validator_simple(data: str) -> str:
                if 'wrong' in data:
                    raise ModelRetry('wrong response')
                return data
    
            @agent.result_validator
            async def result_validator_deps(ctx: RunContext[str], data: str) -> str:
                if ctx.deps in data:
                    raise ModelRetry('wrong response')
                return data
    
            result = agent.run_sync('foobar', deps='spam')
            print(result.data)
            #> success (no tool calls)
            ```
            """
            self._result_validators.append(_result.ResultValidator(func))
            return func
    
        @overload
        def tool(self, func: ToolFuncContext[AgentDeps, ToolParams], /) -> ToolFuncContext[AgentDeps, ToolParams]: ...
    
        @overload
        def tool(
            self,
            /,
            *,
            retries: int | None = None,
            prepare: ToolPrepareFunc[AgentDeps] | None = None,
        ) -> Callable[[ToolFuncContext[AgentDeps, ToolParams]], ToolFuncContext[AgentDeps, ToolParams]]: ...
    
        def tool(
            self,
            func: ToolFuncContext[AgentDeps, ToolParams] | None = None,
            /,
            *,
            retries: int | None = None,
            prepare: ToolPrepareFunc[AgentDeps] | None = None,
        ) -> Any:
            """Decorator to register a tool function which takes [`RunContext`][pydantic_ai.tools.RunContext] as its first argument.
    
            Can decorate a sync or async functions.
    
            The docstring is inspected to extract both the tool description and description of each parameter,
            [learn more](../tools.md#function-tools-and-schema).
    
            We can't add overloads for every possible signature of tool, since the return type is a recursive union
            so the signature of functions decorated with `@agent.tool` is obscured.
    
            Example:
            ```python
            from pydantic_ai import Agent, RunContext
    
            agent = Agent('test', deps_type=int)
    
            @agent.tool
            def foobar(ctx: RunContext[int], x: int) -> int:
                return ctx.deps + x
    
            @agent.tool(retries=2)
            async def spam(ctx: RunContext[str], y: float) -> float:
                return ctx.deps + y
    
            result = agent.run_sync('foobar', deps=1)
            print(result.data)
            #> {"foobar":1,"spam":1.0}
            ```
    
            Args:
                func: The tool function to register.
                retries: The number of retries to allow for this tool, defaults to the agent's default retries,
                    which defaults to 1.
                prepare: custom method to prepare the tool definition for each step, return `None` to omit this
                    tool from a given step. This is useful if you want to customise a tool at call time,
                    or omit it completely from a step. See [`ToolPrepareFunc`][pydantic_ai.tools.ToolPrepareFunc].
            """
            if func is None:
    
                def tool_decorator(
                    func_: ToolFuncContext[AgentDeps, ToolParams],
                ) -> ToolFuncContext[AgentDeps, ToolParams]:
                    # noinspection PyTypeChecker
                    self._register_function(func_, True, retries, prepare)
                    return func_
    
                return tool_decorator
            else:
                # noinspection PyTypeChecker
                self._register_function(func, True, retries, prepare)
                return func
    
        @overload
        def tool_plain(self, func: ToolFuncPlain[ToolParams], /) -> ToolFuncPlain[ToolParams]: ...
    
        @overload
        def tool_plain(
            self,
            /,
            *,
            retries: int | None = None,
            prepare: ToolPrepareFunc[AgentDeps] | None = None,
        ) -> Callable[[ToolFuncPlain[ToolParams]], ToolFuncPlain[ToolParams]]: ...
    
        def tool_plain(
            self,
            func: ToolFuncPlain[ToolParams] | None = None,
            /,
            *,
            retries: int | None = None,
            prepare: ToolPrepareFunc[AgentDeps] | None = None,
        ) -> Any:
            """Decorator to register a tool function which DOES NOT take `RunContext` as an argument.
    
            Can decorate a sync or async functions.
    
            The docstring is inspected to extract both the tool description and description of each parameter,
            [learn more](../tools.md#function-tools-and-schema).
    
            We can't add overloads for every possible signature of tool, since the return type is a recursive union
            so the signature of functions decorated with `@agent.tool` is obscured.
    
            Example:
            ```python
            from pydantic_ai import Agent, RunContext
    
            agent = Agent('test')
    
            @agent.tool
            def foobar(ctx: RunContext[int]) -> int:
                return 123
    
            @agent.tool(retries=2)
            async def spam(ctx: RunContext[str]) -> float:
                return 3.14
    
            result = agent.run_sync('foobar', deps=1)
            print(result.data)
            #> {"foobar":123,"spam":3.14}
            ```
    
            Args:
                func: The tool function to register.
                retries: The number of retries to allow for this tool, defaults to the agent's default retries,
                    which defaults to 1.
                prepare: custom method to prepare the tool definition for each step, return `None` to omit this
                    tool from a given step. This is useful if you want to customise a tool at call time,
                    or omit it completely from a step. See [`ToolPrepareFunc`][pydantic_ai.tools.ToolPrepareFunc].
            """
            if func is None:
    
                def tool_decorator(func_: ToolFuncPlain[ToolParams]) -> ToolFuncPlain[ToolParams]:
                    # noinspection PyTypeChecker
                    self._register_function(func_, False, retries, prepare)
                    return func_
    
                return tool_decorator
            else:
                self._register_function(func, False, retries, prepare)
                return func
    
        def _register_function(
            self,
            func: ToolFuncEither[AgentDeps, ToolParams],
            takes_ctx: bool,
            retries: int | None,
            prepare: ToolPrepareFunc[AgentDeps] | None,
        ) -> None:
            """Private utility to register a function as a tool."""
            retries_ = retries if retries is not None else self._default_retries
            tool = Tool(func, takes_ctx=takes_ctx, max_retries=retries_, prepare=prepare)
            self._register_tool(tool)
    
        def _register_tool(self, tool: Tool[AgentDeps]) -> None:
            """Private utility to register a tool instance."""
            if tool.max_retries is None:
                # noinspection PyTypeChecker
                tool = dataclasses.replace(tool, max_retries=self._default_retries)
    
            if tool.name in self._function_tools:
                raise exceptions.UserError(f'Tool name conflicts with existing tool: {tool.name!r}')
    
            if self._result_schema and tool.name in self._result_schema.tools:
                raise exceptions.UserError(f'Tool name conflicts with result schema name: {tool.name!r}')
    
            self._function_tools[tool.name] = tool
    
        async def _get_model(self, model: models.Model | models.KnownModelName | None) -> tuple[models.Model, str]:
            """Create a model configured for this agent.
    
            Args:
                model: model to use for this run, required if `model` was not set when creating the agent.
    
            Returns:
                a tuple of `(model used, how the model was selected)`
            """
            model_: models.Model
            if some_model := self._override_model:
                # we don't want `override()` to cover up errors from the model not being defined, hence this check
                if model is None and self.model is None:
                    raise exceptions.UserError(
                        '`model` must be set either when creating the agent or when calling it. '
                        '(Even when `override(model=...)` is customizing the model that will actually be called)'
                    )
                model_ = some_model.value
                mode_selection = 'override-model'
            elif model is not None:
                model_ = models.infer_model(model)
                mode_selection = 'custom'
            elif self.model is not None:
                # noinspection PyTypeChecker
                model_ = self.model = models.infer_model(self.model)
                mode_selection = 'from-agent'
            else:
                raise exceptions.UserError('`model` must be set either when creating the agent or when calling it.')
    
            return model_, mode_selection
    
        async def _prepare_model(self, run_context: RunContext[AgentDeps]) -> models.AgentModel:
            """Build tools and create an agent model."""
            function_tools: list[ToolDefinition] = []
    
            async def add_tool(tool: Tool[AgentDeps]) -> None:
                ctx = run_context.replace_with(retry=tool.current_retry, tool_name=tool.name)
                if tool_def := await tool.prepare_tool_def(ctx):
                    function_tools.append(tool_def)
    
            await asyncio.gather(*map(add_tool, self._function_tools.values()))
    
            return await run_context.model.agent_model(
                function_tools=function_tools,
                allow_text_result=self._allow_text_result,
                result_tools=self._result_schema.tool_defs() if self._result_schema is not None else [],
            )
    
        async def _prepare_messages(
            self, user_prompt: str, message_history: list[_messages.ModelMessage] | None, run_context: RunContext[AgentDeps]
        ) -> list[_messages.ModelMessage]:
            if message_history:
                # shallow copy messages
                messages = message_history.copy()
                messages.append(_messages.ModelRequest([_messages.UserPromptPart(user_prompt)]))
            else:
                parts = await self._sys_parts(run_context)
                parts.append(_messages.UserPromptPart(user_prompt))
                messages: list[_messages.ModelMessage] = [_messages.ModelRequest(parts)]
    
            return messages
    
        async def _handle_model_response(
            self, model_response: _messages.ModelResponse, run_context: RunContext[AgentDeps]
        ) -> tuple[_MarkFinalResult[ResultData] | None, list[_messages.ModelRequestPart]]:
            """Process a non-streamed response from the model.
    
            Returns:
                A tuple of `(final_result, request parts)`. If `final_result` is not `None`, the conversation should end.
            """
            texts: list[str] = []
            tool_calls: list[_messages.ToolCallPart] = []
            for part in model_response.parts:
                if isinstance(part, _messages.TextPart):
                    # ignore empty content for text parts, see #437
                    if part.content:
                        texts.append(part.content)
                else:
                    tool_calls.append(part)
    
            # At the moment, we prioritize at least executing tool calls if they are present.
            # In the future, we'd consider making this configurable at the agent or run level.
            # This accounts for cases like anthropic returns that might contain a text response
            # and a tool call response, where the text response just indicates the tool call will happen.
            if tool_calls:
                return await self._handle_structured_response(tool_calls, run_context)
            elif texts:
                text = '\n\n'.join(texts)
                return await self._handle_text_response(text, run_context)
            else:
                raise exceptions.UnexpectedModelBehavior('Received empty model response')
    
        async def _handle_text_response(
            self, text: str, run_context: RunContext[AgentDeps]
        ) -> tuple[_MarkFinalResult[ResultData] | None, list[_messages.ModelRequestPart]]:
            """Handle a plain text response from the model for non-streaming responses."""
            if self._allow_text_result:
                result_data_input = cast(ResultData, text)
                try:
                    result_data = await self._validate_result(result_data_input, run_context, None)
                except _result.ToolRetryError as e:
                    self._incr_result_retry(run_context)
                    return None, [e.tool_retry]
                else:
                    return _MarkFinalResult(result_data, None), []
            else:
                self._incr_result_retry(run_context)
                response = _messages.RetryPromptPart(
                    content='Plain text responses are not permitted, please call one of the functions instead.',
                )
                return None, [response]
    
        async def _handle_structured_response(
            self, tool_calls: list[_messages.ToolCallPart], run_context: RunContext[AgentDeps]
        ) -> tuple[_MarkFinalResult[ResultData] | None, list[_messages.ModelRequestPart]]:
            """Handle a structured response containing tool calls from the model for non-streaming responses."""
            assert tool_calls, 'Expected at least one tool call'
    
            # first look for the result tool call
            final_result: _MarkFinalResult[ResultData] | None = None
    
            parts: list[_messages.ModelRequestPart] = []
            if result_schema := self._result_schema:
                if match := result_schema.find_tool(tool_calls):
                    call, result_tool = match
                    try:
                        result_data = result_tool.validate(call)
                        result_data = await self._validate_result(result_data, run_context, call)
                    except _result.ToolRetryError as e:
                        self._incr_result_retry(run_context)
                        parts.append(e.tool_retry)
                    else:
                        final_result = _MarkFinalResult(result_data, call.tool_name)
    
            # Then build the other request parts based on end strategy
            parts += await self._process_function_tools(tool_calls, final_result and final_result.tool_name, run_context)
    
            return final_result, parts
    
        async def _process_function_tools(
            self,
            tool_calls: list[_messages.ToolCallPart],
            result_tool_name: str | None,
            run_context: RunContext[AgentDeps],
        ) -> list[_messages.ModelRequestPart]:
            """Process function (non-result) tool calls in parallel.
    
            Also add stub return parts for any other tools that need it.
            """
            parts: list[_messages.ModelRequestPart] = []
            tasks: list[asyncio.Task[_messages.ModelRequestPart]] = []
    
            stub_function_tools = bool(result_tool_name) and self.end_strategy == 'early'
    
            # we rely on the fact that if we found a result, it's the first result tool in the last
            found_used_result_tool = False
            for call in tool_calls:
                if call.tool_name == result_tool_name and not found_used_result_tool:
                    found_used_result_tool = True
                    parts.append(
                        _messages.ToolReturnPart(
                            tool_name=call.tool_name,
                            content='Final result processed.',
                            tool_call_id=call.tool_call_id,
                        )
                    )
                elif tool := self._function_tools.get(call.tool_name):
                    if stub_function_tools:
                        parts.append(
                            _messages.ToolReturnPart(
                                tool_name=call.tool_name,
                                content='Tool not executed - a final result was already processed.',
                                tool_call_id=call.tool_call_id,
                            )
                        )
                    else:
                        tasks.append(asyncio.create_task(tool.run(call, run_context), name=call.tool_name))
                elif self._result_schema is not None and call.tool_name in self._result_schema.tools:
                    # if tool_name is in _result_schema, it means we found a result tool but an error occurred in
                    # validation, we don't add another part here
                    if result_tool_name is not None:
                        parts.append(
                            _messages.ToolReturnPart(
                                tool_name=call.tool_name,
                                content='Result tool not used - a final result was already processed.',
                                tool_call_id=call.tool_call_id,
                            )
                        )
                else:
                    parts.append(self._unknown_tool(call.tool_name, run_context))
    
            # Run all tool tasks in parallel
            if tasks:
                with _logfire.span('running {tools=}', tools=[t.get_name() for t in tasks]):
                    task_results: Sequence[_messages.ModelRequestPart] = await asyncio.gather(*tasks)
                    parts.extend(task_results)
            return parts
    
        async def _handle_streamed_model_response(
            self,
            model_response: models.EitherStreamedResponse,
            run_context: RunContext[AgentDeps],
        ) -> (
            _MarkFinalResult[models.EitherStreamedResponse]
            | tuple[_messages.ModelResponse, list[_messages.ModelRequestPart]]
        ):
            """Process a streamed response from the model.
    
            Returns:
                Either a final result or a tuple of the model response and the tool responses for the next request.
                If a final result is returned, the conversation should end.
            """
            if isinstance(model_response, models.StreamTextResponse):
                # plain string response
                if self._allow_text_result:
                    return _MarkFinalResult(model_response, None)
                else:
                    self._incr_result_retry(run_context)
                    response = _messages.RetryPromptPart(
                        content='Plain text responses are not permitted, please call one of the functions instead.',
                    )
                    # stream the response, so usage is correct
                    async for _ in model_response:
                        pass
    
                    text = ''.join(model_response.get(final=True))
                    return _messages.ModelResponse([_messages.TextPart(text)]), [response]
            elif isinstance(model_response, models.StreamStructuredResponse):
                if self._result_schema is not None:
                    # if there's a result schema, iterate over the stream until we find at least one tool
                    # NOTE: this means we ignore any other tools called here
                    structured_msg = model_response.get()
                    while not structured_msg.parts:
                        try:
                            await model_response.__anext__()
                        except StopAsyncIteration:
                            break
                        structured_msg = model_response.get()
    
                    if match := self._result_schema.find_tool(structured_msg.parts):
                        call, _ = match
                        return _MarkFinalResult(model_response, call.tool_name)
    
                # the model is calling a tool function, consume the response to get the next message
                async for _ in model_response:
                    pass
                model_response_msg = model_response.get()
                if not model_response_msg.parts:
                    raise exceptions.UnexpectedModelBehavior('Received empty tool call message')
    
                # we now run all tool functions in parallel
                tasks: list[asyncio.Task[_messages.ModelRequestPart]] = []
                parts: list[_messages.ModelRequestPart] = []
                for item in model_response_msg.parts:
                    if isinstance(item, _messages.ToolCallPart):
                        call = item
                        if tool := self._function_tools.get(call.tool_name):
                            tasks.append(asyncio.create_task(tool.run(call, run_context), name=call.tool_name))
                        else:
                            parts.append(self._unknown_tool(call.tool_name, run_context))
    
                with _logfire.span('running {tools=}', tools=[t.get_name() for t in tasks]):
                    task_results: Sequence[_messages.ModelRequestPart] = await asyncio.gather(*tasks)
                    parts.extend(task_results)
                return model_response_msg, parts
            else:
                assert_never(model_response)
    
        async def _validate_result(
            self,
            result_data: ResultData,
            run_context: RunContext[AgentDeps],
            tool_call: _messages.ToolCallPart | None,
        ) -> ResultData:
            for validator in self._result_validators:
                result_data = await validator.validate(result_data, tool_call, run_context)
            return result_data
    
        def _incr_result_retry(self, run_context: RunContext[AgentDeps]) -> None:
            run_context.retry += 1
            if run_context.retry > self._max_result_retries:
                raise exceptions.UnexpectedModelBehavior(
                    f'Exceeded maximum retries ({self._max_result_retries}) for result validation'
                )
    
        async def _sys_parts(self, run_context: RunContext[AgentDeps]) -> list[_messages.ModelRequestPart]:
            """Build the initial messages for the conversation."""
            messages: list[_messages.ModelRequestPart] = [_messages.SystemPromptPart(p) for p in self._system_prompts]
            for sys_prompt_runner in self._system_prompt_functions:
                prompt = await sys_prompt_runner.run(run_context)
                messages.append(_messages.SystemPromptPart(prompt))
            return messages
    
        def _unknown_tool(self, tool_name: str, run_context: RunContext[AgentDeps]) -> _messages.RetryPromptPart:
            self._incr_result_retry(run_context)
            names = list(self._function_tools.keys())
            if self._result_schema:
                names.extend(self._result_schema.tool_names())
            if names:
                msg = f'Available tools: {", ".join(names)}'
            else:
                msg = 'No tools available.'
            return _messages.RetryPromptPart(content=f'Unknown tool name: {tool_name!r}. {msg}')
    
        def _get_deps(self, deps: AgentDeps) -> AgentDeps:
            """Get deps for a run.
    
            If we've overridden deps via `_override_deps`, use that, otherwise use the deps passed to the call.
    
            We could do runtime type checking of deps against `self._deps_type`, but that's a slippery slope.
            """
            if some_deps := self._override_deps:
                return some_deps.value
            else:
                return deps
    
        def _infer_name(self, function_frame: FrameType | None) -> None:
            """Infer the agent name from the call frame.
    
            Usage should be `self._infer_name(inspect.currentframe())`.
            """
            assert self.name is None, 'Name already set'
            if function_frame is not None:  # pragma: no branch
                if parent_frame := function_frame.f_back:  # pragma: no branch
                    for name, item in parent_frame.f_locals.items():
                        if item is self:
                            self.name = name
                            return
                    if parent_frame.f_locals != parent_frame.f_globals:
                        # if we couldn't find the agent in locals and globals are a different dict, try globals
                        for name, item in parent_frame.f_globals.items():
                            if item is self:
                                self.name = name
                                return
      
  
---|---  
  
###  __init__

    
    
    __init__(
        model: [Model](../models/base/#pydantic_ai.models.Model "pydantic_ai.models.Model") | [KnownModelName](../models/base/#pydantic_ai.models.KnownModelName "pydantic_ai.models.KnownModelName") | None = None,
        *,
        result_type: [type](https://docs.python.org/3/library/functions.html#type)[[ResultData](../result/#pydantic_ai.result.ResultData "pydantic_ai.result.ResultData")] = [str](https://docs.python.org/3/library/stdtypes.html#str),
        system_prompt: [str](https://docs.python.org/3/library/stdtypes.html#str) | [Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence "collections.abc.Sequence")[[str](https://docs.python.org/3/library/stdtypes.html#str)] = (),
        deps_type: [type](https://docs.python.org/3/library/functions.html#type)[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps")] = NoneType,
        name: [str](https://docs.python.org/3/library/stdtypes.html#str) | None = None,
        model_settings: [ModelSettings](../settings/#pydantic_ai.settings.ModelSettings "pydantic_ai.settings.ModelSettings") | None = None,
        retries: [int](https://docs.python.org/3/library/functions.html#int) = 1,
        result_tool_name: [str](https://docs.python.org/3/library/stdtypes.html#str) = "final_result",
        result_tool_description: [str](https://docs.python.org/3/library/stdtypes.html#str) | None = None,
        result_retries: [int](https://docs.python.org/3/library/functions.html#int) | None = None,
        tools: [Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence "collections.abc.Sequence")[
            [Tool](../tools/#pydantic_ai.tools.Tool "pydantic_ai.tools.Tool")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps")] | [ToolFuncEither](../tools/#pydantic_ai.tools.ToolFuncEither "pydantic_ai.tools.ToolFuncEither")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps"), ...]
        ] = (),
        defer_model_check: [bool](https://docs.python.org/3/library/functions.html#bool) = False,
        end_strategy: EndStrategy = "early"
    )
    

Create an agent.

Parameters:

Name | Type | Description | Default  
---|---|---|---  
`model` |  `[Model](../models/base/#pydantic_ai.models.Model "pydantic_ai.models.Model") | [KnownModelName](../models/base/#pydantic_ai.models.KnownModelName "pydantic_ai.models.KnownModelName") | None` |  The default model to use for this agent, if not provide, you must provide the model when calling it. |  `None`  
`result_type` |  `[type](https://docs.python.org/3/library/functions.html#type)[[ResultData](../result/#pydantic_ai.result.ResultData "pydantic_ai.result.ResultData")]` |  The type of the result data, used to validate the result data, defaults to `str`. |  `[str](https://docs.python.org/3/library/stdtypes.html#str)`  
`system_prompt` |  `[str](https://docs.python.org/3/library/stdtypes.html#str) | [Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence "collections.abc.Sequence")[[str](https://docs.python.org/3/library/stdtypes.html#str)]` |  Static system prompts to use for this agent, you can also register system prompts via a function with `system_prompt`. |  `()`  
`deps_type` |  `[type](https://docs.python.org/3/library/functions.html#type)[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps")]` |  The type used for dependency injection, this parameter exists solely to allow you to fully parameterize the agent, and therefore get the best out of static type checking. If you're not using deps, but want type checking to pass, you can set `deps=None` to satisfy Pyright or add a type hint `: Agent[None, <return type>]`. |  `NoneType`  
`name` |  `[str](https://docs.python.org/3/library/stdtypes.html#str) | None` |  The name of the agent, used for logging. If `None`, we try to infer the agent name from the call frame when the agent is first run. |  `None`  
`model_settings` |  `[ModelSettings](../settings/#pydantic_ai.settings.ModelSettings "pydantic_ai.settings.ModelSettings") | None` |  Optional model request settings to use for this agent's runs, by default. |  `None`  
`retries` |  `[int](https://docs.python.org/3/library/functions.html#int)` |  The default number of retries to allow before raising an error. |  `1`  
`result_tool_name` |  `[str](https://docs.python.org/3/library/stdtypes.html#str)` |  The name of the tool to use for the final result. |  `'final_result'`  
`result_tool_description` |  `[str](https://docs.python.org/3/library/stdtypes.html#str) | None` |  The description of the final result tool. |  `None`  
`result_retries` |  `[int](https://docs.python.org/3/library/functions.html#int) | None` |  The maximum number of retries to allow for result validation, defaults to `retries`. |  `None`  
`tools` |  `[Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence "collections.abc.Sequence")[[Tool](../tools/#pydantic_ai.tools.Tool "pydantic_ai.tools.Tool")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps")] | [ToolFuncEither](../tools/#pydantic_ai.tools.ToolFuncEither "pydantic_ai.tools.ToolFuncEither")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps"), ...]]` |  Tools to register with the agent, you can also register tools via the decorators `@agent.tool` and `@agent.tool_plain`. |  `()`  
`defer_model_check` |  `[bool](https://docs.python.org/3/library/functions.html#bool)` |  by default, if you provide a [named](../models/base/#pydantic_ai.models.KnownModelName) model, it's evaluated to create a [`Model`](../models/base/#pydantic_ai.models.Model) instance immediately, which checks for the necessary environment variables. Set this to `false` to defer the evaluation until the first run. Useful if you want to override the model for testing. |  `False`  
`end_strategy` |  `EndStrategy` |  Strategy for handling tool calls that are requested alongside a final result. See `EndStrategy` for more information. |  `'early'`  
  
Source code in `pydantic_ai_slim/pydantic_ai/agent.py`

    
    
    110
    111
    112
    113
    114
    115
    116
    117
    118
    119
    120
    121
    122
    123
    124
    125
    126
    127
    128
    129
    130
    131
    132
    133
    134
    135
    136
    137
    138
    139
    140
    141
    142
    143
    144
    145
    146
    147
    148
    149
    150
    151
    152
    153
    154
    155
    156
    157
    158
    159
    160
    161
    162
    163
    164
    165
    166
    167
    168
    169
    170
    171
    172
    173
    174
    175
    176
    177
    178
    179
    180
    181
    182

|

    
    
    def __init__(
        self,
        model: models.Model | models.KnownModelName | None = None,
        *,
        result_type: type[ResultData] = str,
        system_prompt: str | Sequence[str] = (),
        deps_type: type[AgentDeps] = NoneType,
        name: str | None = None,
        model_settings: ModelSettings | None = None,
        retries: int = 1,
        result_tool_name: str = 'final_result',
        result_tool_description: str | None = None,
        result_retries: int | None = None,
        tools: Sequence[Tool[AgentDeps] | ToolFuncEither[AgentDeps, ...]] = (),
        defer_model_check: bool = False,
        end_strategy: EndStrategy = 'early',
    ):
        """Create an agent.
    
        Args:
            model: The default model to use for this agent, if not provide,
                you must provide the model when calling it.
            result_type: The type of the result data, used to validate the result data, defaults to `str`.
            system_prompt: Static system prompts to use for this agent, you can also register system
                prompts via a function with [`system_prompt`][pydantic_ai.Agent.system_prompt].
            deps_type: The type used for dependency injection, this parameter exists solely to allow you to fully
                parameterize the agent, and therefore get the best out of static type checking.
                If you're not using deps, but want type checking to pass, you can set `deps=None` to satisfy Pyright
                or add a type hint `: Agent[None, <return type>]`.
            name: The name of the agent, used for logging. If `None`, we try to infer the agent name from the call frame
                when the agent is first run.
            model_settings: Optional model request settings to use for this agent's runs, by default.
            retries: The default number of retries to allow before raising an error.
            result_tool_name: The name of the tool to use for the final result.
            result_tool_description: The description of the final result tool.
            result_retries: The maximum number of retries to allow for result validation, defaults to `retries`.
            tools: Tools to register with the agent, you can also register tools via the decorators
                [`@agent.tool`][pydantic_ai.Agent.tool] and [`@agent.tool_plain`][pydantic_ai.Agent.tool_plain].
            defer_model_check: by default, if you provide a [named][pydantic_ai.models.KnownModelName] model,
                it's evaluated to create a [`Model`][pydantic_ai.models.Model] instance immediately,
                which checks for the necessary environment variables. Set this to `false`
                to defer the evaluation until the first run. Useful if you want to
                [override the model][pydantic_ai.Agent.override] for testing.
            end_strategy: Strategy for handling tool calls that are requested alongside a final result.
                See [`EndStrategy`][pydantic_ai.agent.EndStrategy] for more information.
        """
        if model is None or defer_model_check:
            self.model = model
        else:
            self.model = models.infer_model(model)
    
        self.end_strategy = end_strategy
        self.name = name
        self.model_settings = model_settings
        self.last_run_messages = None
        self._result_schema = _result.ResultSchema[result_type].build(
            result_type, result_tool_name, result_tool_description
        )
        # if the result tool is None, or its schema allows `str`, we allow plain text results
        self._allow_text_result = self._result_schema is None or self._result_schema.allow_text_result
    
        self._system_prompts = (system_prompt,) if isinstance(system_prompt, str) else tuple(system_prompt)
        self._function_tools = {}
        self._default_retries = retries
        for tool in tools:
            if isinstance(tool, Tool):
                self._register_tool(tool)
            else:
                self._register_tool(Tool(tool))
        self._deps_type = deps_type
        self._system_prompt_functions = []
        self._max_result_retries = result_retries if result_retries is not None else retries
        self._result_validators = []
      
  
---|---  
  
###  name `instance-attribute`

    
    
    name: [str](https://docs.python.org/3/library/stdtypes.html#str) | None = name
    

The name of the agent, used for logging.

If `None`, we try to infer the agent name from the call frame when the agent
is first run.

###  run `async`

    
    
    run(
        user_prompt: [str](https://docs.python.org/3/library/stdtypes.html#str),
        *,
        message_history: [list](https://docs.python.org/3/library/stdtypes.html#list)[[ModelMessage](../messages/#pydantic_ai.messages.ModelMessage "pydantic_ai.messages.ModelMessage")] | None = None,
        model: [Model](../models/base/#pydantic_ai.models.Model "pydantic_ai.models.Model") | [KnownModelName](../models/base/#pydantic_ai.models.KnownModelName "pydantic_ai.models.KnownModelName") | None = None,
        deps: [AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps") = None,
        model_settings: [ModelSettings](../settings/#pydantic_ai.settings.ModelSettings "pydantic_ai.settings.ModelSettings") | None = None,
        usage_limits: [UsageLimits](../settings/#pydantic_ai.settings.UsageLimits "pydantic_ai.settings.UsageLimits") | None = None,
        infer_name: [bool](https://docs.python.org/3/library/functions.html#bool) = True
    ) -> [RunResult](../result/#pydantic_ai.result.RunResult "pydantic_ai.result.RunResult")[[ResultData](../result/#pydantic_ai.result.ResultData "pydantic_ai.result.ResultData")]
    

Run the agent with a user prompt in async mode.

Example:

    
    
    from pydantic_ai import Agent
    
    agent = Agent('openai:gpt-4o')
    
    result_sync = agent.run_sync('What is the capital of Italy?')
    print(result_sync.data)
    #> Rome
    

Parameters:

Name | Type | Description | Default  
---|---|---|---  
`user_prompt` |  `[str](https://docs.python.org/3/library/stdtypes.html#str)` |  User input to start/continue the conversation. |  _required_  
`message_history` |  `[list](https://docs.python.org/3/library/stdtypes.html#list)[[ModelMessage](../messages/#pydantic_ai.messages.ModelMessage "pydantic_ai.messages.ModelMessage")] | None` |  History of the conversation so far. |  `None`  
`model` |  `[Model](../models/base/#pydantic_ai.models.Model "pydantic_ai.models.Model") | [KnownModelName](../models/base/#pydantic_ai.models.KnownModelName "pydantic_ai.models.KnownModelName") | None` |  Optional model to use for this run, required if `model` was not set when creating the agent. |  `None`  
`deps` |  `[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps")` |  Optional dependencies to use for this run. |  `None`  
`model_settings` |  `[ModelSettings](../settings/#pydantic_ai.settings.ModelSettings "pydantic_ai.settings.ModelSettings") | None` |  Optional settings to use for this model's request. |  `None`  
`usage_limits` |  `[UsageLimits](../settings/#pydantic_ai.settings.UsageLimits "pydantic_ai.settings.UsageLimits") | None` |  Optional limits on model request count or token usage. |  `None`  
`infer_name` |  `[bool](https://docs.python.org/3/library/functions.html#bool)` |  Whether to try to infer the agent name from the call frame if it's not set. |  `True`  
  
Returns:

Type | Description  
---|---  
`[RunResult](../result/#pydantic_ai.result.RunResult "pydantic_ai.result.RunResult")[[ResultData](../result/#pydantic_ai.result.ResultData "pydantic_ai.result.ResultData")]` |  The result of the run.  
  
Source code in `pydantic_ai_slim/pydantic_ai/agent.py`

    
    
    184
    185
    186
    187
    188
    189
    190
    191
    192
    193
    194
    195
    196
    197
    198
    199
    200
    201
    202
    203
    204
    205
    206
    207
    208
    209
    210
    211
    212
    213
    214
    215
    216
    217
    218
    219
    220
    221
    222
    223
    224
    225
    226
    227
    228
    229
    230
    231
    232
    233
    234
    235
    236
    237
    238
    239
    240
    241
    242
    243
    244
    245
    246
    247
    248
    249
    250
    251
    252
    253
    254
    255
    256
    257
    258
    259
    260
    261
    262
    263
    264
    265
    266
    267
    268
    269
    270
    271
    272
    273
    274
    275
    276
    277
    278
    279
    280
    281
    282
    283

|

    
    
    async def run(
        self,
        user_prompt: str,
        *,
        message_history: list[_messages.ModelMessage] | None = None,
        model: models.Model | models.KnownModelName | None = None,
        deps: AgentDeps = None,
        model_settings: ModelSettings | None = None,
        usage_limits: UsageLimits | None = None,
        infer_name: bool = True,
    ) -> result.RunResult[ResultData]:
        """Run the agent with a user prompt in async mode.
    
        Example:
        ```python
        from pydantic_ai import Agent
    
        agent = Agent('openai:gpt-4o')
    
        result_sync = agent.run_sync('What is the capital of Italy?')
        print(result_sync.data)
        #> Rome
        ```
    
        Args:
            user_prompt: User input to start/continue the conversation.
            message_history: History of the conversation so far.
            model: Optional model to use for this run, required if `model` was not set when creating the agent.
            deps: Optional dependencies to use for this run.
            model_settings: Optional settings to use for this model's request.
            usage_limits: Optional limits on model request count or token usage.
            infer_name: Whether to try to infer the agent name from the call frame if it's not set.
    
        Returns:
            The result of the run.
        """
        if infer_name and self.name is None:
            self._infer_name(inspect.currentframe())
        model_used, mode_selection = await self._get_model(model)
    
        deps = self._get_deps(deps)
        new_message_index = len(message_history) if message_history else 0
    
        with _logfire.span(
            '{agent_name} run {prompt=}',
            prompt=user_prompt,
            agent=self,
            mode_selection=mode_selection,
            model_name=model_used.name(),
            agent_name=self.name or 'agent',
        ) as run_span:
            run_context = RunContext(deps, 0, [], None, model_used)
            messages = await self._prepare_messages(user_prompt, message_history, run_context)
            self.last_run_messages = run_context.messages = messages
    
            for tool in self._function_tools.values():
                tool.current_retry = 0
    
            usage = result.Usage(requests=0)
            model_settings = merge_model_settings(self.model_settings, model_settings)
            usage_limits = usage_limits or UsageLimits()
    
            run_step = 0
            while True:
                usage_limits.check_before_request(usage)
    
                run_step += 1
                with _logfire.span('preparing model and tools {run_step=}', run_step=run_step):
                    agent_model = await self._prepare_model(run_context)
    
                with _logfire.span('model request', run_step=run_step) as model_req_span:
                    model_response, request_usage = await agent_model.request(messages, model_settings)
                    model_req_span.set_attribute('response', model_response)
                    model_req_span.set_attribute('usage', request_usage)
    
                messages.append(model_response)
                usage += request_usage
                usage.requests += 1
                usage_limits.check_tokens(request_usage)
    
                with _logfire.span('handle model response', run_step=run_step) as handle_span:
                    final_result, tool_responses = await self._handle_model_response(model_response, run_context)
    
                    if tool_responses:
                        # Add parts to the conversation as a new message
                        messages.append(_messages.ModelRequest(tool_responses))
    
                    # Check if we got a final result
                    if final_result is not None:
                        result_data = final_result.data
                        run_span.set_attribute('all_messages', messages)
                        run_span.set_attribute('usage', usage)
                        handle_span.set_attribute('result', result_data)
                        handle_span.message = 'handle model response -> final result'
                        return result.RunResult(messages, new_message_index, result_data, usage)
                    else:
                        # continue the conversation
                        handle_span.set_attribute('tool_responses', tool_responses)
                        tool_responses_str = ' '.join(r.part_kind for r in tool_responses)
                        handle_span.message = f'handle model response -> {tool_responses_str}'
      
  
---|---  
  
###  run_sync

    
    
    run_sync(
        user_prompt: [str](https://docs.python.org/3/library/stdtypes.html#str),
        *,
        message_history: [list](https://docs.python.org/3/library/stdtypes.html#list)[[ModelMessage](../messages/#pydantic_ai.messages.ModelMessage "pydantic_ai.messages.ModelMessage")] | None = None,
        model: [Model](../models/base/#pydantic_ai.models.Model "pydantic_ai.models.Model") | [KnownModelName](../models/base/#pydantic_ai.models.KnownModelName "pydantic_ai.models.KnownModelName") | None = None,
        deps: [AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps") = None,
        model_settings: [ModelSettings](../settings/#pydantic_ai.settings.ModelSettings "pydantic_ai.settings.ModelSettings") | None = None,
        usage_limits: [UsageLimits](../settings/#pydantic_ai.settings.UsageLimits "pydantic_ai.settings.UsageLimits") | None = None,
        infer_name: [bool](https://docs.python.org/3/library/functions.html#bool) = True
    ) -> [RunResult](../result/#pydantic_ai.result.RunResult "pydantic_ai.result.RunResult")[[ResultData](../result/#pydantic_ai.result.ResultData "pydantic_ai.result.ResultData")]
    

Run the agent with a user prompt synchronously.

This is a convenience method that wraps `self.run` with
`loop.run_until_complete(...)`. You therefore can't use this method inside
async code or if there's an active event loop.

Example:

    
    
    from pydantic_ai import Agent
    
    agent = Agent('openai:gpt-4o')
    
    async def main():
        result = await agent.run('What is the capital of France?')
        print(result.data)
        #> Paris
    

Parameters:

Name | Type | Description | Default  
---|---|---|---  
`user_prompt` |  `[str](https://docs.python.org/3/library/stdtypes.html#str)` |  User input to start/continue the conversation. |  _required_  
`message_history` |  `[list](https://docs.python.org/3/library/stdtypes.html#list)[[ModelMessage](../messages/#pydantic_ai.messages.ModelMessage "pydantic_ai.messages.ModelMessage")] | None` |  History of the conversation so far. |  `None`  
`model` |  `[Model](../models/base/#pydantic_ai.models.Model "pydantic_ai.models.Model") | [KnownModelName](../models/base/#pydantic_ai.models.KnownModelName "pydantic_ai.models.KnownModelName") | None` |  Optional model to use for this run, required if `model` was not set when creating the agent. |  `None`  
`deps` |  `[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps")` |  Optional dependencies to use for this run. |  `None`  
`model_settings` |  `[ModelSettings](../settings/#pydantic_ai.settings.ModelSettings "pydantic_ai.settings.ModelSettings") | None` |  Optional settings to use for this model's request. |  `None`  
`usage_limits` |  `[UsageLimits](../settings/#pydantic_ai.settings.UsageLimits "pydantic_ai.settings.UsageLimits") | None` |  Optional limits on model request count or token usage. |  `None`  
`infer_name` |  `[bool](https://docs.python.org/3/library/functions.html#bool)` |  Whether to try to infer the agent name from the call frame if it's not set. |  `True`  
  
Returns:

Type | Description  
---|---  
`[RunResult](../result/#pydantic_ai.result.RunResult "pydantic_ai.result.RunResult")[[ResultData](../result/#pydantic_ai.result.ResultData "pydantic_ai.result.ResultData")]` |  The result of the run.  
  
Source code in `pydantic_ai_slim/pydantic_ai/agent.py`

    
    
    285
    286
    287
    288
    289
    290
    291
    292
    293
    294
    295
    296
    297
    298
    299
    300
    301
    302
    303
    304
    305
    306
    307
    308
    309
    310
    311
    312
    313
    314
    315
    316
    317
    318
    319
    320
    321
    322
    323
    324
    325
    326
    327
    328
    329
    330
    331
    332
    333
    334
    335
    336
    337

|

    
    
    def run_sync(
        self,
        user_prompt: str,
        *,
        message_history: list[_messages.ModelMessage] | None = None,
        model: models.Model | models.KnownModelName | None = None,
        deps: AgentDeps = None,
        model_settings: ModelSettings | None = None,
        usage_limits: UsageLimits | None = None,
        infer_name: bool = True,
    ) -> result.RunResult[ResultData]:
        """Run the agent with a user prompt synchronously.
    
        This is a convenience method that wraps [`self.run`][pydantic_ai.Agent.run] with `loop.run_until_complete(...)`.
        You therefore can't use this method inside async code or if there's an active event loop.
    
        Example:
        ```python
        from pydantic_ai import Agent
    
        agent = Agent('openai:gpt-4o')
    
        async def main():
            result = await agent.run('What is the capital of France?')
            print(result.data)
            #> Paris
        ```
    
        Args:
            user_prompt: User input to start/continue the conversation.
            message_history: History of the conversation so far.
            model: Optional model to use for this run, required if `model` was not set when creating the agent.
            deps: Optional dependencies to use for this run.
            model_settings: Optional settings to use for this model's request.
            usage_limits: Optional limits on model request count or token usage.
            infer_name: Whether to try to infer the agent name from the call frame if it's not set.
    
        Returns:
            The result of the run.
        """
        if infer_name and self.name is None:
            self._infer_name(inspect.currentframe())
        return asyncio.get_event_loop().run_until_complete(
            self.run(
                user_prompt,
                message_history=message_history,
                model=model,
                deps=deps,
                model_settings=model_settings,
                usage_limits=usage_limits,
                infer_name=False,
            )
        )
      
  
---|---  
  
###  run_stream `async`

    
    
    run_stream(
        user_prompt: [str](https://docs.python.org/3/library/stdtypes.html#str),
        *,
        message_history: [list](https://docs.python.org/3/library/stdtypes.html#list)[[ModelMessage](../messages/#pydantic_ai.messages.ModelMessage "pydantic_ai.messages.ModelMessage")] | None = None,
        model: [Model](../models/base/#pydantic_ai.models.Model "pydantic_ai.models.Model") | [KnownModelName](../models/base/#pydantic_ai.models.KnownModelName "pydantic_ai.models.KnownModelName") | None = None,
        deps: [AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps") = None,
        model_settings: [ModelSettings](../settings/#pydantic_ai.settings.ModelSettings "pydantic_ai.settings.ModelSettings") | None = None,
        usage_limits: [UsageLimits](../settings/#pydantic_ai.settings.UsageLimits "pydantic_ai.settings.UsageLimits") | None = None,
        infer_name: [bool](https://docs.python.org/3/library/functions.html#bool) = True
    ) -> [AsyncIterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.AsyncIterator "collections.abc.AsyncIterator")[
        [StreamedRunResult](../result/#pydantic_ai.result.StreamedRunResult "pydantic_ai.result.StreamedRunResult")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps"), [ResultData](../result/#pydantic_ai.result.ResultData "pydantic_ai.result.ResultData")]
    ]
    

Run the agent with a user prompt in async mode, returning a streamed response.

Example:

    
    
    from pydantic_ai import Agent
    
    agent = Agent('openai:gpt-4o')
    
    async def main():
        async with agent.run_stream('What is the capital of the UK?') as response:
            print(await response.get_data())
            #> London
    

Parameters:

Name | Type | Description | Default  
---|---|---|---  
`user_prompt` |  `[str](https://docs.python.org/3/library/stdtypes.html#str)` |  User input to start/continue the conversation. |  _required_  
`message_history` |  `[list](https://docs.python.org/3/library/stdtypes.html#list)[[ModelMessage](../messages/#pydantic_ai.messages.ModelMessage "pydantic_ai.messages.ModelMessage")] | None` |  History of the conversation so far. |  `None`  
`model` |  `[Model](../models/base/#pydantic_ai.models.Model "pydantic_ai.models.Model") | [KnownModelName](../models/base/#pydantic_ai.models.KnownModelName "pydantic_ai.models.KnownModelName") | None` |  Optional model to use for this run, required if `model` was not set when creating the agent. |  `None`  
`deps` |  `[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps")` |  Optional dependencies to use for this run. |  `None`  
`model_settings` |  `[ModelSettings](../settings/#pydantic_ai.settings.ModelSettings "pydantic_ai.settings.ModelSettings") | None` |  Optional settings to use for this model's request. |  `None`  
`usage_limits` |  `[UsageLimits](../settings/#pydantic_ai.settings.UsageLimits "pydantic_ai.settings.UsageLimits") | None` |  Optional limits on model request count or token usage. |  `None`  
`infer_name` |  `[bool](https://docs.python.org/3/library/functions.html#bool)` |  Whether to try to infer the agent name from the call frame if it's not set. |  `True`  
  
Returns:

Type | Description  
---|---  
`[AsyncIterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.AsyncIterator "collections.abc.AsyncIterator")[[StreamedRunResult](../result/#pydantic_ai.result.StreamedRunResult "pydantic_ai.result.StreamedRunResult")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps"), [ResultData](../result/#pydantic_ai.result.ResultData "pydantic_ai.result.ResultData")]]` |  The result of the run.  
  
Source code in `pydantic_ai_slim/pydantic_ai/agent.py`

    
    
    339
    340
    341
    342
    343
    344
    345
    346
    347
    348
    349
    350
    351
    352
    353
    354
    355
    356
    357
    358
    359
    360
    361
    362
    363
    364
    365
    366
    367
    368
    369
    370
    371
    372
    373
    374
    375
    376
    377
    378
    379
    380
    381
    382
    383
    384
    385
    386
    387
    388
    389
    390
    391
    392
    393
    394
    395
    396
    397
    398
    399
    400
    401
    402
    403
    404
    405
    406
    407
    408
    409
    410
    411
    412
    413
    414
    415
    416
    417
    418
    419
    420
    421
    422
    423
    424
    425
    426
    427
    428
    429
    430
    431
    432
    433
    434
    435
    436
    437
    438
    439
    440
    441
    442
    443
    444
    445
    446
    447
    448
    449
    450
    451
    452
    453
    454
    455
    456
    457
    458
    459
    460
    461
    462
    463
    464
    465
    466
    467
    468
    469
    470
    471
    472
    473
    474
    475
    476

|

    
    
    @asynccontextmanager
    async def run_stream(
        self,
        user_prompt: str,
        *,
        message_history: list[_messages.ModelMessage] | None = None,
        model: models.Model | models.KnownModelName | None = None,
        deps: AgentDeps = None,
        model_settings: ModelSettings | None = None,
        usage_limits: UsageLimits | None = None,
        infer_name: bool = True,
    ) -> AsyncIterator[result.StreamedRunResult[AgentDeps, ResultData]]:
        """Run the agent with a user prompt in async mode, returning a streamed response.
    
        Example:
        ```python
        from pydantic_ai import Agent
    
        agent = Agent('openai:gpt-4o')
    
        async def main():
            async with agent.run_stream('What is the capital of the UK?') as response:
                print(await response.get_data())
                #> London
        ```
    
        Args:
            user_prompt: User input to start/continue the conversation.
            message_history: History of the conversation so far.
            model: Optional model to use for this run, required if `model` was not set when creating the agent.
            deps: Optional dependencies to use for this run.
            model_settings: Optional settings to use for this model's request.
            usage_limits: Optional limits on model request count or token usage.
            infer_name: Whether to try to infer the agent name from the call frame if it's not set.
    
        Returns:
            The result of the run.
        """
        if infer_name and self.name is None:
            # f_back because `asynccontextmanager` adds one frame
            if frame := inspect.currentframe():  # pragma: no branch
                self._infer_name(frame.f_back)
        model_used, mode_selection = await self._get_model(model)
    
        deps = self._get_deps(deps)
        new_message_index = len(message_history) if message_history else 0
    
        with _logfire.span(
            '{agent_name} run stream {prompt=}',
            prompt=user_prompt,
            agent=self,
            mode_selection=mode_selection,
            model_name=model_used.name(),
            agent_name=self.name or 'agent',
        ) as run_span:
            run_context = RunContext(deps, 0, [], None, model_used)
            messages = await self._prepare_messages(user_prompt, message_history, run_context)
            self.last_run_messages = run_context.messages = messages
    
            for tool in self._function_tools.values():
                tool.current_retry = 0
    
            usage = result.Usage()
            model_settings = merge_model_settings(self.model_settings, model_settings)
            usage_limits = usage_limits or UsageLimits()
    
            run_step = 0
            while True:
                run_step += 1
                usage_limits.check_before_request(usage)
    
                with _logfire.span('preparing model and tools {run_step=}', run_step=run_step):
                    agent_model = await self._prepare_model(run_context)
    
                with _logfire.span('model request {run_step=}', run_step=run_step) as model_req_span:
                    async with agent_model.request_stream(messages, model_settings) as model_response:
                        usage.requests += 1
                        model_req_span.set_attribute('response_type', model_response.__class__.__name__)
                        # We want to end the "model request" span here, but we can't exit the context manager
                        # in the traditional way
                        model_req_span.__exit__(None, None, None)
    
                        with _logfire.span('handle model response') as handle_span:
                            maybe_final_result = await self._handle_streamed_model_response(model_response, run_context)
    
                            # Check if we got a final result
                            if isinstance(maybe_final_result, _MarkFinalResult):
                                result_stream = maybe_final_result.data
                                result_tool_name = maybe_final_result.tool_name
                                handle_span.message = 'handle model response -> final result'
    
                                async def on_complete():
                                    """Called when the stream has completed.
    
                                    The model response will have been added to messages by now
                                    by `StreamedRunResult._marked_completed`.
                                    """
                                    last_message = messages[-1]
                                    assert isinstance(last_message, _messages.ModelResponse)
                                    tool_calls = [
                                        part for part in last_message.parts if isinstance(part, _messages.ToolCallPart)
                                    ]
                                    parts = await self._process_function_tools(
                                        tool_calls, result_tool_name, run_context
                                    )
                                    if parts:
                                        messages.append(_messages.ModelRequest(parts))
                                    run_span.set_attribute('all_messages', messages)
    
                                yield result.StreamedRunResult(
                                    messages,
                                    new_message_index,
                                    usage,
                                    usage_limits,
                                    result_stream,
                                    self._result_schema,
                                    run_context,
                                    self._result_validators,
                                    result_tool_name,
                                    on_complete,
                                )
                                return
                            else:
                                # continue the conversation
                                model_response_msg, tool_responses = maybe_final_result
                                # if we got a model response add that to messages
                                messages.append(model_response_msg)
                                if tool_responses:
                                    # if we got one or more tool response parts, add a model request message
                                    messages.append(_messages.ModelRequest(tool_responses))
    
                                handle_span.set_attribute('tool_responses', tool_responses)
                                tool_responses_str = ' '.join(r.part_kind for r in tool_responses)
                                handle_span.message = f'handle model response -> {tool_responses_str}'
                                # the model_response should have been fully streamed by now, we can add its usage
                                model_response_usage = model_response.usage()
                                usage += model_response_usage
                                usage_limits.check_tokens(usage)
      
  
---|---  
  
###  model `instance-attribute`

    
    
    model: [Model](../models/base/#pydantic_ai.models.Model "pydantic_ai.models.Model") | [KnownModelName](../models/base/#pydantic_ai.models.KnownModelName "pydantic_ai.models.KnownModelName") | None
    

The default model configured for this agent.

###  override

    
    
    override(
        *,
        deps: [AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps") | Unset = UNSET,
        model: [Model](../models/base/#pydantic_ai.models.Model "pydantic_ai.models.Model") | [KnownModelName](../models/base/#pydantic_ai.models.KnownModelName "pydantic_ai.models.KnownModelName") | Unset = UNSET
    ) -> [Iterator](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator "collections.abc.Iterator")[None]
    

Context manager to temporarily override agent dependencies and model.

This is particularly useful when testing. You can find an example of this
[here](../../testing-evals/#overriding-model-via-pytest-fixtures).

Parameters:

Name | Type | Description | Default  
---|---|---|---  
`deps` |  `[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps") | Unset` |  The dependencies to use instead of the dependencies passed to the agent run. |  `UNSET`  
`model` |  `[Model](../models/base/#pydantic_ai.models.Model "pydantic_ai.models.Model") | [KnownModelName](../models/base/#pydantic_ai.models.KnownModelName "pydantic_ai.models.KnownModelName") | Unset` |  The model to use instead of the model passed to the agent run. |  `UNSET`  
  
Source code in `pydantic_ai_slim/pydantic_ai/agent.py`

    
    
    478
    479
    480
    481
    482
    483
    484
    485
    486
    487
    488
    489
    490
    491
    492
    493
    494
    495
    496
    497
    498
    499
    500
    501
    502
    503
    504
    505
    506
    507
    508
    509
    510
    511
    512
    513
    514

|

    
    
    @contextmanager
    def override(
        self,
        *,
        deps: AgentDeps | _utils.Unset = _utils.UNSET,
        model: models.Model | models.KnownModelName | _utils.Unset = _utils.UNSET,
    ) -> Iterator[None]:
        """Context manager to temporarily override agent dependencies and model.
    
        This is particularly useful when testing.
        You can find an example of this [here](../testing-evals.md#overriding-model-via-pytest-fixtures).
    
        Args:
            deps: The dependencies to use instead of the dependencies passed to the agent run.
            model: The model to use instead of the model passed to the agent run.
        """
        if _utils.is_set(deps):
            override_deps_before = self._override_deps
            self._override_deps = _utils.Some(deps)
        else:
            override_deps_before = _utils.UNSET
    
        # noinspection PyTypeChecker
        if _utils.is_set(model):
            override_model_before = self._override_model
            # noinspection PyTypeChecker
            self._override_model = _utils.Some(models.infer_model(model))  # pyright: ignore[reportArgumentType]
        else:
            override_model_before = _utils.UNSET
    
        try:
            yield
        finally:
            if _utils.is_set(override_deps_before):
                self._override_deps = override_deps_before
            if _utils.is_set(override_model_before):
                self._override_model = override_model_before
      
  
---|---  
  
###  last_run_messages `instance-attribute`

    
    
    last_run_messages: [list](https://docs.python.org/3/library/stdtypes.html#list)[[ModelMessage](../messages/#pydantic_ai.messages.ModelMessage "pydantic_ai.messages.ModelMessage")] | None = None
    

The messages from the last run, useful when a run raised an exception.

Note: these are not used by the agent, e.g. in future runs, they are just
stored for developers' convenience.

###  system_prompt

    
    
    system_prompt(
        func: [Callable](https://docs.python.org/3/library/typing.html#typing.Callable "typing.Callable")[[[RunContext](../tools/#pydantic_ai.tools.RunContext "pydantic_ai.tools.RunContext")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps")]], [str](https://docs.python.org/3/library/stdtypes.html#str)]
    ) -> [Callable](https://docs.python.org/3/library/typing.html#typing.Callable "typing.Callable")[[[RunContext](../tools/#pydantic_ai.tools.RunContext "pydantic_ai.tools.RunContext")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps")]], [str](https://docs.python.org/3/library/stdtypes.html#str)]
    
    
    
    system_prompt(
        func: [Callable](https://docs.python.org/3/library/typing.html#typing.Callable "typing.Callable")[[[RunContext](../tools/#pydantic_ai.tools.RunContext "pydantic_ai.tools.RunContext")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps")]], [Awaitable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "collections.abc.Awaitable")[[str](https://docs.python.org/3/library/stdtypes.html#str)]]
    ) -> [Callable](https://docs.python.org/3/library/typing.html#typing.Callable "typing.Callable")[[[RunContext](../tools/#pydantic_ai.tools.RunContext "pydantic_ai.tools.RunContext")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps")]], [Awaitable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "collections.abc.Awaitable")[[str](https://docs.python.org/3/library/stdtypes.html#str)]]
    
    
    
    system_prompt(func: [Callable](https://docs.python.org/3/library/typing.html#typing.Callable "typing.Callable")[[], [str](https://docs.python.org/3/library/stdtypes.html#str)]) -> [Callable](https://docs.python.org/3/library/typing.html#typing.Callable "typing.Callable")[[], [str](https://docs.python.org/3/library/stdtypes.html#str)]
    
    
    
    system_prompt(
        func: [Callable](https://docs.python.org/3/library/typing.html#typing.Callable "typing.Callable")[[], [Awaitable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "collections.abc.Awaitable")[[str](https://docs.python.org/3/library/stdtypes.html#str)]]
    ) -> [Callable](https://docs.python.org/3/library/typing.html#typing.Callable "typing.Callable")[[], [Awaitable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "collections.abc.Awaitable")[[str](https://docs.python.org/3/library/stdtypes.html#str)]]
    
    
    
    system_prompt(
        func: [SystemPromptFunc](../tools/#pydantic_ai.tools.SystemPromptFunc "pydantic_ai._system_prompt.SystemPromptFunc")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps")],
    ) -> [SystemPromptFunc](../tools/#pydantic_ai.tools.SystemPromptFunc "pydantic_ai._system_prompt.SystemPromptFunc")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps")]
    

Decorator to register a system prompt function.

Optionally takes [`RunContext`](../tools/#pydantic_ai.tools.RunContext) as its
only argument. Can decorate a sync or async functions.

Overloads for every possible signature of `system_prompt` are included so the
decorator doesn't obscure the type of the function, see `tests/typed_agent.py`
for tests.

Example:

    
    
    from pydantic_ai import Agent, RunContext
    
    agent = Agent('test', deps_type=str)
    
    @agent.system_prompt
    def simple_system_prompt() -> str:
        return 'foobar'
    
    @agent.system_prompt
    async def async_system_prompt(ctx: RunContext[str]) -> str:
        return f'{ctx.deps} is the best'
    
    result = agent.run_sync('foobar', deps='spam')
    print(result.data)
    #> success (no tool calls)
    

Source code in `pydantic_ai_slim/pydantic_ai/agent.py`

    
    
    532
    533
    534
    535
    536
    537
    538
    539
    540
    541
    542
    543
    544
    545
    546
    547
    548
    549
    550
    551
    552
    553
    554
    555
    556
    557
    558
    559
    560
    561
    562
    563

|

    
    
    def system_prompt(
        self, func: _system_prompt.SystemPromptFunc[AgentDeps], /
    ) -> _system_prompt.SystemPromptFunc[AgentDeps]:
        """Decorator to register a system prompt function.
    
        Optionally takes [`RunContext`][pydantic_ai.tools.RunContext] as its only argument.
        Can decorate a sync or async functions.
    
        Overloads for every possible signature of `system_prompt` are included so the decorator doesn't obscure
        the type of the function, see `tests/typed_agent.py` for tests.
    
        Example:
        ```python
        from pydantic_ai import Agent, RunContext
    
        agent = Agent('test', deps_type=str)
    
        @agent.system_prompt
        def simple_system_prompt() -> str:
            return 'foobar'
    
        @agent.system_prompt
        async def async_system_prompt(ctx: RunContext[str]) -> str:
            return f'{ctx.deps} is the best'
    
        result = agent.run_sync('foobar', deps='spam')
        print(result.data)
        #> success (no tool calls)
        ```
        """
        self._system_prompt_functions.append(_system_prompt.SystemPromptRunner(func))
        return func
      
  
---|---  
  
###  tool

    
    
    tool(
        func: [ToolFuncContext](../tools/#pydantic_ai.tools.ToolFuncContext "pydantic_ai.tools.ToolFuncContext")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps"), [ToolParams](../tools/#pydantic_ai.tools.ToolParams "pydantic_ai.tools.ToolParams")]
    ) -> [ToolFuncContext](../tools/#pydantic_ai.tools.ToolFuncContext "pydantic_ai.tools.ToolFuncContext")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps"), [ToolParams](../tools/#pydantic_ai.tools.ToolParams "pydantic_ai.tools.ToolParams")]
    
    
    
    tool(
        *,
        retries: [int](https://docs.python.org/3/library/functions.html#int) | None = None,
        prepare: [ToolPrepareFunc](../tools/#pydantic_ai.tools.ToolPrepareFunc "pydantic_ai.tools.ToolPrepareFunc")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps")] | None = None
    ) -> [Callable](https://docs.python.org/3/library/typing.html#typing.Callable "typing.Callable")[
        [[ToolFuncContext](../tools/#pydantic_ai.tools.ToolFuncContext "pydantic_ai.tools.ToolFuncContext")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps"), [ToolParams](../tools/#pydantic_ai.tools.ToolParams "pydantic_ai.tools.ToolParams")]],
        [ToolFuncContext](../tools/#pydantic_ai.tools.ToolFuncContext "pydantic_ai.tools.ToolFuncContext")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps"), [ToolParams](../tools/#pydantic_ai.tools.ToolParams "pydantic_ai.tools.ToolParams")],
    ]
    
    
    
    tool(
        func: (
            [ToolFuncContext](../tools/#pydantic_ai.tools.ToolFuncContext "pydantic_ai.tools.ToolFuncContext")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps"), [ToolParams](../tools/#pydantic_ai.tools.ToolParams "pydantic_ai.tools.ToolParams")] | None
        ) = None,
        /,
        *,
        retries: [int](https://docs.python.org/3/library/functions.html#int) | None = None,
        prepare: [ToolPrepareFunc](../tools/#pydantic_ai.tools.ToolPrepareFunc "pydantic_ai.tools.ToolPrepareFunc")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps")] | None = None,
    ) -> [Any](https://docs.python.org/3/library/typing.html#typing.Any "typing.Any")
    

Decorator to register a tool function which takes
[`RunContext`](../tools/#pydantic_ai.tools.RunContext) as its first argument.

Can decorate a sync or async functions.

The docstring is inspected to extract both the tool description and
description of each parameter, [learn more](../../tools/#function-tools-and-
schema).

We can't add overloads for every possible signature of tool, since the return
type is a recursive union so the signature of functions decorated with
`@agent.tool` is obscured.

Example:

    
    
    from pydantic_ai import Agent, RunContext
    
    agent = Agent('test', deps_type=int)
    
    @agent.tool
    def foobar(ctx: RunContext[int], x: int) -> int:
        return ctx.deps + x
    
    @agent.tool(retries=2)
    async def spam(ctx: RunContext[str], y: float) -> float:
        return ctx.deps + y
    
    result = agent.run_sync('foobar', deps=1)
    print(result.data)
    #> {"foobar":1,"spam":1.0}
    

Parameters:

Name | Type | Description | Default  
---|---|---|---  
`func` |  `[ToolFuncContext](../tools/#pydantic_ai.tools.ToolFuncContext "pydantic_ai.tools.ToolFuncContext")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps"), [ToolParams](../tools/#pydantic_ai.tools.ToolParams "pydantic_ai.tools.ToolParams")] | None` |  The tool function to register. |  `None`  
`retries` |  `[int](https://docs.python.org/3/library/functions.html#int) | None` |  The number of retries to allow for this tool, defaults to the agent's default retries, which defaults to 1. |  `None`  
`prepare` |  `[ToolPrepareFunc](../tools/#pydantic_ai.tools.ToolPrepareFunc "pydantic_ai.tools.ToolPrepareFunc")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps")] | None` |  custom method to prepare the tool definition for each step, return `None` to omit this tool from a given step. This is useful if you want to customise a tool at call time, or omit it completely from a step. See [`ToolPrepareFunc`](../tools/#pydantic_ai.tools.ToolPrepareFunc). |  `None`  
  
Source code in `pydantic_ai_slim/pydantic_ai/agent.py`

    
    
    632
    633
    634
    635
    636
    637
    638
    639
    640
    641
    642
    643
    644
    645
    646
    647
    648
    649
    650
    651
    652
    653
    654
    655
    656
    657
    658
    659
    660
    661
    662
    663
    664
    665
    666
    667
    668
    669
    670
    671
    672
    673
    674
    675
    676
    677
    678
    679
    680
    681
    682
    683
    684
    685
    686
    687
    688
    689
    690

|

    
    
    def tool(
        self,
        func: ToolFuncContext[AgentDeps, ToolParams] | None = None,
        /,
        *,
        retries: int | None = None,
        prepare: ToolPrepareFunc[AgentDeps] | None = None,
    ) -> Any:
        """Decorator to register a tool function which takes [`RunContext`][pydantic_ai.tools.RunContext] as its first argument.
    
        Can decorate a sync or async functions.
    
        The docstring is inspected to extract both the tool description and description of each parameter,
        [learn more](../tools.md#function-tools-and-schema).
    
        We can't add overloads for every possible signature of tool, since the return type is a recursive union
        so the signature of functions decorated with `@agent.tool` is obscured.
    
        Example:
        ```python
        from pydantic_ai import Agent, RunContext
    
        agent = Agent('test', deps_type=int)
    
        @agent.tool
        def foobar(ctx: RunContext[int], x: int) -> int:
            return ctx.deps + x
    
        @agent.tool(retries=2)
        async def spam(ctx: RunContext[str], y: float) -> float:
            return ctx.deps + y
    
        result = agent.run_sync('foobar', deps=1)
        print(result.data)
        #> {"foobar":1,"spam":1.0}
        ```
    
        Args:
            func: The tool function to register.
            retries: The number of retries to allow for this tool, defaults to the agent's default retries,
                which defaults to 1.
            prepare: custom method to prepare the tool definition for each step, return `None` to omit this
                tool from a given step. This is useful if you want to customise a tool at call time,
                or omit it completely from a step. See [`ToolPrepareFunc`][pydantic_ai.tools.ToolPrepareFunc].
        """
        if func is None:
    
            def tool_decorator(
                func_: ToolFuncContext[AgentDeps, ToolParams],
            ) -> ToolFuncContext[AgentDeps, ToolParams]:
                # noinspection PyTypeChecker
                self._register_function(func_, True, retries, prepare)
                return func_
    
            return tool_decorator
        else:
            # noinspection PyTypeChecker
            self._register_function(func, True, retries, prepare)
            return func
      
  
---|---  
  
###  tool_plain

    
    
    tool_plain(
        func: [ToolFuncPlain](../tools/#pydantic_ai.tools.ToolFuncPlain "pydantic_ai.tools.ToolFuncPlain")[[ToolParams](../tools/#pydantic_ai.tools.ToolParams "pydantic_ai.tools.ToolParams")],
    ) -> [ToolFuncPlain](../tools/#pydantic_ai.tools.ToolFuncPlain "pydantic_ai.tools.ToolFuncPlain")[[ToolParams](../tools/#pydantic_ai.tools.ToolParams "pydantic_ai.tools.ToolParams")]
    
    
    
    tool_plain(
        *,
        retries: [int](https://docs.python.org/3/library/functions.html#int) | None = None,
        prepare: [ToolPrepareFunc](../tools/#pydantic_ai.tools.ToolPrepareFunc "pydantic_ai.tools.ToolPrepareFunc")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps")] | None = None
    ) -> [Callable](https://docs.python.org/3/library/typing.html#typing.Callable "typing.Callable")[
        [[ToolFuncPlain](../tools/#pydantic_ai.tools.ToolFuncPlain "pydantic_ai.tools.ToolFuncPlain")[[ToolParams](../tools/#pydantic_ai.tools.ToolParams "pydantic_ai.tools.ToolParams")]], [ToolFuncPlain](../tools/#pydantic_ai.tools.ToolFuncPlain "pydantic_ai.tools.ToolFuncPlain")[[ToolParams](../tools/#pydantic_ai.tools.ToolParams "pydantic_ai.tools.ToolParams")]
    ]
    
    
    
    tool_plain(
        func: [ToolFuncPlain](../tools/#pydantic_ai.tools.ToolFuncPlain "pydantic_ai.tools.ToolFuncPlain")[[ToolParams](../tools/#pydantic_ai.tools.ToolParams "pydantic_ai.tools.ToolParams")] | None = None,
        /,
        *,
        retries: [int](https://docs.python.org/3/library/functions.html#int) | None = None,
        prepare: [ToolPrepareFunc](../tools/#pydantic_ai.tools.ToolPrepareFunc "pydantic_ai.tools.ToolPrepareFunc")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps")] | None = None,
    ) -> [Any](https://docs.python.org/3/library/typing.html#typing.Any "typing.Any")
    

Decorator to register a tool function which DOES NOT take `RunContext` as an
argument.

Can decorate a sync or async functions.

The docstring is inspected to extract both the tool description and
description of each parameter, [learn more](../../tools/#function-tools-and-
schema).

We can't add overloads for every possible signature of tool, since the return
type is a recursive union so the signature of functions decorated with
`@agent.tool` is obscured.

Example:

    
    
    from pydantic_ai import Agent, RunContext
    
    agent = Agent('test')
    
    @agent.tool
    def foobar(ctx: RunContext[int]) -> int:
        return 123
    
    @agent.tool(retries=2)
    async def spam(ctx: RunContext[str]) -> float:
        return 3.14
    
    result = agent.run_sync('foobar', deps=1)
    print(result.data)
    #> {"foobar":123,"spam":3.14}
    

Parameters:

Name | Type | Description | Default  
---|---|---|---  
`func` |  `[ToolFuncPlain](../tools/#pydantic_ai.tools.ToolFuncPlain "pydantic_ai.tools.ToolFuncPlain")[[ToolParams](../tools/#pydantic_ai.tools.ToolParams "pydantic_ai.tools.ToolParams")] | None` |  The tool function to register. |  `None`  
`retries` |  `[int](https://docs.python.org/3/library/functions.html#int) | None` |  The number of retries to allow for this tool, defaults to the agent's default retries, which defaults to 1. |  `None`  
`prepare` |  `[ToolPrepareFunc](../tools/#pydantic_ai.tools.ToolPrepareFunc "pydantic_ai.tools.ToolPrepareFunc")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps")] | None` |  custom method to prepare the tool definition for each step, return `None` to omit this tool from a given step. This is useful if you want to customise a tool at call time, or omit it completely from a step. See [`ToolPrepareFunc`](../tools/#pydantic_ai.tools.ToolPrepareFunc). |  `None`  
  
Source code in `pydantic_ai_slim/pydantic_ai/agent.py`

    
    
    704
    705
    706
    707
    708
    709
    710
    711
    712
    713
    714
    715
    716
    717
    718
    719
    720
    721
    722
    723
    724
    725
    726
    727
    728
    729
    730
    731
    732
    733
    734
    735
    736
    737
    738
    739
    740
    741
    742
    743
    744
    745
    746
    747
    748
    749
    750
    751
    752
    753
    754
    755
    756
    757
    758
    759

|

    
    
    def tool_plain(
        self,
        func: ToolFuncPlain[ToolParams] | None = None,
        /,
        *,
        retries: int | None = None,
        prepare: ToolPrepareFunc[AgentDeps] | None = None,
    ) -> Any:
        """Decorator to register a tool function which DOES NOT take `RunContext` as an argument.
    
        Can decorate a sync or async functions.
    
        The docstring is inspected to extract both the tool description and description of each parameter,
        [learn more](../tools.md#function-tools-and-schema).
    
        We can't add overloads for every possible signature of tool, since the return type is a recursive union
        so the signature of functions decorated with `@agent.tool` is obscured.
    
        Example:
        ```python
        from pydantic_ai import Agent, RunContext
    
        agent = Agent('test')
    
        @agent.tool
        def foobar(ctx: RunContext[int]) -> int:
            return 123
    
        @agent.tool(retries=2)
        async def spam(ctx: RunContext[str]) -> float:
            return 3.14
    
        result = agent.run_sync('foobar', deps=1)
        print(result.data)
        #> {"foobar":123,"spam":3.14}
        ```
    
        Args:
            func: The tool function to register.
            retries: The number of retries to allow for this tool, defaults to the agent's default retries,
                which defaults to 1.
            prepare: custom method to prepare the tool definition for each step, return `None` to omit this
                tool from a given step. This is useful if you want to customise a tool at call time,
                or omit it completely from a step. See [`ToolPrepareFunc`][pydantic_ai.tools.ToolPrepareFunc].
        """
        if func is None:
    
            def tool_decorator(func_: ToolFuncPlain[ToolParams]) -> ToolFuncPlain[ToolParams]:
                # noinspection PyTypeChecker
                self._register_function(func_, False, retries, prepare)
                return func_
    
            return tool_decorator
        else:
            self._register_function(func, False, retries, prepare)
            return func
      
  
---|---  
  
###  result_validator

    
    
    result_validator(
        func: [Callable](https://docs.python.org/3/library/typing.html#typing.Callable "typing.Callable")[
            [[RunContext](../tools/#pydantic_ai.tools.RunContext "pydantic_ai.tools.RunContext")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps")], [ResultData](../result/#pydantic_ai.result.ResultData "pydantic_ai.result.ResultData")], [ResultData](../result/#pydantic_ai.result.ResultData "pydantic_ai.result.ResultData")
        ]
    ) -> [Callable](https://docs.python.org/3/library/typing.html#typing.Callable "typing.Callable")[
        [[RunContext](../tools/#pydantic_ai.tools.RunContext "pydantic_ai.tools.RunContext")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps")], [ResultData](../result/#pydantic_ai.result.ResultData "pydantic_ai.result.ResultData")], [ResultData](../result/#pydantic_ai.result.ResultData "pydantic_ai.result.ResultData")
    ]
    
    
    
    result_validator(
        func: [Callable](https://docs.python.org/3/library/typing.html#typing.Callable "typing.Callable")[
            [[RunContext](../tools/#pydantic_ai.tools.RunContext "pydantic_ai.tools.RunContext")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps")], [ResultData](../result/#pydantic_ai.result.ResultData "pydantic_ai.result.ResultData")],
            [Awaitable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "collections.abc.Awaitable")[[ResultData](../result/#pydantic_ai.result.ResultData "pydantic_ai.result.ResultData")],
        ]
    ) -> [Callable](https://docs.python.org/3/library/typing.html#typing.Callable "typing.Callable")[
        [[RunContext](../tools/#pydantic_ai.tools.RunContext "pydantic_ai.tools.RunContext")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps")], [ResultData](../result/#pydantic_ai.result.ResultData "pydantic_ai.result.ResultData")],
        [Awaitable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "collections.abc.Awaitable")[[ResultData](../result/#pydantic_ai.result.ResultData "pydantic_ai.result.ResultData")],
    ]
    
    
    
    result_validator(
        func: [Callable](https://docs.python.org/3/library/typing.html#typing.Callable "typing.Callable")[[[ResultData](../result/#pydantic_ai.result.ResultData "pydantic_ai.result.ResultData")], [ResultData](../result/#pydantic_ai.result.ResultData "pydantic_ai.result.ResultData")]
    ) -> [Callable](https://docs.python.org/3/library/typing.html#typing.Callable "typing.Callable")[[[ResultData](../result/#pydantic_ai.result.ResultData "pydantic_ai.result.ResultData")], [ResultData](../result/#pydantic_ai.result.ResultData "pydantic_ai.result.ResultData")]
    
    
    
    result_validator(
        func: [Callable](https://docs.python.org/3/library/typing.html#typing.Callable "typing.Callable")[[[ResultData](../result/#pydantic_ai.result.ResultData "pydantic_ai.result.ResultData")], [Awaitable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "collections.abc.Awaitable")[[ResultData](../result/#pydantic_ai.result.ResultData "pydantic_ai.result.ResultData")]]
    ) -> [Callable](https://docs.python.org/3/library/typing.html#typing.Callable "typing.Callable")[[[ResultData](../result/#pydantic_ai.result.ResultData "pydantic_ai.result.ResultData")], [Awaitable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "collections.abc.Awaitable")[[ResultData](../result/#pydantic_ai.result.ResultData "pydantic_ai.result.ResultData")]]
    
    
    
    result_validator(
        func: [ResultValidatorFunc](../result/#pydantic_ai.result.ResultValidatorFunc "pydantic_ai._result.ResultValidatorFunc")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps"), [ResultData](../result/#pydantic_ai.result.ResultData "pydantic_ai.result.ResultData")]
    ) -> [ResultValidatorFunc](../result/#pydantic_ai.result.ResultValidatorFunc "pydantic_ai._result.ResultValidatorFunc")[[AgentDeps](../tools/#pydantic_ai.tools.AgentDeps "pydantic_ai.tools.AgentDeps"), [ResultData](../result/#pydantic_ai.result.ResultData "pydantic_ai.result.ResultData")]
    

Decorator to register a result validator function.

Optionally takes [`RunContext`](../tools/#pydantic_ai.tools.RunContext) as its
first argument. Can decorate a sync or async functions.

Overloads for every possible signature of `result_validator` are included so
the decorator doesn't obscure the type of the function, see
`tests/typed_agent.py` for tests.

Example:

    
    
    from pydantic_ai import Agent, ModelRetry, RunContext
    
    agent = Agent('test', deps_type=str)
    
    @agent.result_validator
    def result_validator_simple(data: str) -> str:
        if 'wrong' in data:
            raise ModelRetry('wrong response')
        return data
    
    @agent.result_validator
    async def result_validator_deps(ctx: RunContext[str], data: str) -> str:
        if ctx.deps in data:
            raise ModelRetry('wrong response')
        return data
    
    result = agent.run_sync('foobar', deps='spam')
    print(result.data)
    #> success (no tool calls)
    

Source code in `pydantic_ai_slim/pydantic_ai/agent.py`

    
    
    583
    584
    585
    586
    587
    588
    589
    590
    591
    592
    593
    594
    595
    596
    597
    598
    599
    600
    601
    602
    603
    604
    605
    606
    607
    608
    609
    610
    611
    612
    613
    614
    615
    616
    617
    618

|

    
    
    def result_validator(
        self, func: _result.ResultValidatorFunc[AgentDeps, ResultData], /
    ) -> _result.ResultValidatorFunc[AgentDeps, ResultData]:
        """Decorator to register a result validator function.
    
        Optionally takes [`RunContext`][pydantic_ai.tools.RunContext] as its first argument.
        Can decorate a sync or async functions.
    
        Overloads for every possible signature of `result_validator` are included so the decorator doesn't obscure
        the type of the function, see `tests/typed_agent.py` for tests.
    
        Example:
        ```python
        from pydantic_ai import Agent, ModelRetry, RunContext
    
        agent = Agent('test', deps_type=str)
    
        @agent.result_validator
        def result_validator_simple(data: str) -> str:
            if 'wrong' in data:
                raise ModelRetry('wrong response')
            return data
    
        @agent.result_validator
        async def result_validator_deps(ctx: RunContext[str], data: str) -> str:
            if ctx.deps in data:
                raise ModelRetry('wrong response')
            return data
    
        result = agent.run_sync('foobar', deps='spam')
        print(result.data)
        #> success (no tool calls)
        ```
        """
        self._result_validators.append(_result.ResultValidator(func))
        return func
      
  
---|---  
  
###  pydantic_ai.agent.EndStrategy `module-attribute`

    
    
    EndStrategy = [Literal](https://docs.python.org/3/library/typing.html#typing.Literal "typing.Literal")['early', 'exhaustive']
    

The strategy for handling multiple tool calls when a final result is found.

  * `'early'`: Stop processing other tool calls once a final result is found
  * `'exhaustive'`: Process all tool calls even after finding a final result

© Pydantic Services Inc. 2024 to present

